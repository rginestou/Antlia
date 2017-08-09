import json
import copy
import os.path
from .message import log, ERROR, WARNING, OK
from .elements.color import Color
from .elements.const import *
from .elements.table import EL_TABLE
from pprint import pprint

# Elements
from .elements.window import Window
from .elements.grid import Grid
from .elements.button import Button

class Parser:
	"""
	The Parser reads the layout and style files and builds
	an array of elements to be displayed in the GUI, taking
	into account the style given by the user.
	"""
	def __init__(self, layout_file_name, style_file_name=None):
		self.style_file_name = style_file_name

		# Check if layout file exists
		if not os.path.exists(layout_file_name + ".lia"):
			log(ERROR, "Layout file does not exist", "Import a valid .lia file")
			exit(1)

		# Check if style file exist
		if style_file_name is not None and not os.path.exists(style_file_name + ".lia"):
			log(ERROR, "Style file does not exist", "Import a valid .lia file")
			exit(1)

		# Transform the user defined layout in array of elements
		self._buildLayout(layout_file_name, style_file_name)

	def _buildLayout(self, layout_file_name, style_file_name):
		"""
		Build an array of element and their rects
		"""

		# Fetch the custom elements
		if style_file_name is not None:
			style_chunks = self._loadStyle(style_file_name)
		else:
			style_chunks = {}

		layout_elements, layout_tree, layout_table, root_indices, root_att = self._loadLayout(layout_file_name, style_chunks, offset=1)

		# Add the window object
		window = Window("window")
		for a in root_att:
			window.setAttribute(a, root_att[a])

		self.layout_elements = [window] + layout_elements
		self.layout_tree = [root_indices] + layout_tree
		self.layout_table = layout_table
		self.layout_table["window"] = 0

	def _loadLayout(self, layout_name, style_chunks, offset=0):
		"""
		Load a template file and parse its content.
		The tree is generated according to the file's structure.
		The elements with no indentation are the root of the file,
		and the root_att are the attributes with no indentation.
		A style can be specified to parse custom elements.
		"""
		# Declare the layout variables
		layout_elements = []
		layout_tree = []
		layout_table = {}
		root_indices = []
		root_att = {}

		index_pile = []
		last_element_indent = -1
		n_element = offset

		def _loadLineInfo(line_number, line, n_lines, off_indent=0):
			# Access out of scope variables
			nonlocal layout_elements, layout_tree, layout_table
			nonlocal root_indices, root_att, index_pile
			nonlocal last_element_indent, n_element

			# Get indent and data of the line
			indent, data = self._parseLine(line)
			indent += off_indent

			if line_number != n_lines-1:
				# Jump to next line if empty or if it is a comment
				if len(data) == 0 or data[0] == "" or data[0][0] == "#":
					line_number += 1
					return

				# If the data doesnt contain two blocks, add empty string
				if len(data) != 2:
					data.append("")

			# Look for indentation differentials
			while last_element_indent >= indent:
				# Fetch last element
				last_element_index = index_pile[-1]
				# This last element is fully setup
				index_pile.pop()

				# Set parent-child relation
				if last_element_indent == 0:
					# Root child
					root_indices.append(last_element_index + offset)
				else:
					# The indent-1 element will have one more child
					parent_element_index = index_pile[-1]
					layout_tree[parent_element_index].append(last_element_index + offset)

				# Repeat the process until the last parent element
				# has the same indentation
				last_element_indent -= 1

			if len(data) != 2:
				# For end of file
				return

			if data[0][0] == ".":
				# Look for new properties
				attribute = data[0][1:]
				attribute_value = data[1]

				if len(index_pile) > 0:
					# This attribute refers to a previous element
					layout_elements[index_pile[-1]].setAttribute(attribute, attribute_value)
				else:
					root_att[attribute] = attribute_value
			else:
				# Look for new element
				element_type = data[0]
				element_name = data[1]

				# Parse this new element
				if element_type in EL_TABLE:
					# Regular element
					layout_elements.append(EL_TABLE[element_type](element_name))
				elif element_type in style_chunks:
					# Curstomed defined element
					definition = style_chunks[element_type]
					layout_elements.append(EL_TABLE[definition[0]](element_name))
				else:
					# Does not exist
					log(ERROR, element_type + " is not a valid element, line " + str(line_number))
					exit(1)

				layout_tree.append([])
				layout_table[element_name] = n_element
				last_element_indent = indent

				# Add its index to the pile
				index_pile.append(n_element - offset)

				n_element += 1

				# Loop through the style if custom element
				if element_type in style_chunks:
					definition = style_chunks[element_type]
					for style_line in definition[1:]:
						_loadLineInfo(line_number, style_line, n_lines, off_indent=indent)

		# Open and read the file
		with open(layout_name + ".lia", "r") as layout_file:
			layout_lines = layout_file.readlines()
			layout_lines.append("\n")

		n_lines = len(layout_lines)

		# Loop through all the lines
		for line_number, line in enumerate(layout_lines):
			_loadLineInfo(line_number, line, n_lines)

		return layout_elements, layout_tree, layout_table, root_indices, root_att

	def _loadStyle(self, style_file_name):
		style_chunks = {}

		# Open and read the file
		with open(style_file_name + ".lia", "r") as style_file:
			style_lines = style_file.readlines()
			style_lines.append("\n")

		n_lines = len(style_lines)
		last_element_name = ""

		# Loop through all the lines
		for line_number, line in enumerate(style_lines):
			indent, data = self._parseLine(line)

			# Jump to next line if empty or if it is a comment
			if len(data) == 0 or data[0] == "" or data[0][0] == "#":
				continue

			# If the data doesnt contain two blocks, add empty string
			if len(data) != 2:
				data.append("")

			if indent == 0:
				# New custom element
				last_element_name = data[1]
				style_chunks[last_element_name] = [data[0]]
			else:
				style_chunks[last_element_name].append(line)

		return style_chunks

	def _parseLine(self, line):
		indent = 0
		while line[indent] == "\t":
			indent += 1
		return indent, line.replace("\t", "").replace("\n", "").split(" ", 1)

	def getHandlers(self):
		return {}

	def getLayoutElements(self):
		return self.layout_elements

	def getLayoutTree(self):
		return self.layout_tree

	def getLayoutTable(self):
		return self.layout_table
