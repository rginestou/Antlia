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
		self.style_chunks = {}
		self.style_element_type = {}
		self._buildLayout(layout_file_name, style_file_name)

	def addElement(self, element_type, element_name, parent, attributes):
		"""
		Add the given element to the existing layout
		"""
		layout_lines = [element_type + " " + element_name]
		for a in attributes:
			layout_lines.append("\t." + a + " " + attributes[a])
		layout_lines.append("\n")
		element_index = len(self.layout_elements)

		# Get element layout
		element_layout, element_tree, element_table, _, _ = self._loadLayout(layout_lines, len(layout_lines), offset=element_index)

		# Append to general layout
		self.layout_tree += element_tree
		self.layout_tree[self.layout_table[parent]].append(element_index)
		self.layout_elements += element_layout
		self.layout_table.update(element_table)

	def _buildLayout(self, layout_file_name, style_file_name):
		"""
		Build an array of element and their rects
		"""

		# Fetch the custom elements
		if style_file_name is not None:
			self.style_chunks, self.style_attributes = self._loadStyle(style_file_name)

		# Open and read the file
		with open(layout_file_name + ".lia", "r") as layout_file:
			layout_lines = layout_file.readlines()
			layout_lines.append("\n")

		n_lines = len(layout_lines)

		layout_elements, layout_tree, layout_table, root_indices, root_att = self._loadLayout(layout_lines, n_lines, offset=1)

		# Add the window object
		window = Window("window")
		for a in root_att:
			window.setAttribute(a, root_att[a])

		self.layout_elements = [window] + layout_elements
		self.layout_tree = [root_indices] + layout_tree
		self.layout_table = layout_table
		self.layout_table["window"] = 0

	def _loadLayout(self, layout_content, n_lines_content, offset=0):
		"""
		Load a template and parse its content.
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
		style_element_indices = []
		style_element_name = []

		index_pile = []
		last_element_indent = -1
		n_element = offset

		def _loadLineInfo(line_number, line, n_lines, off_indent=0, prefix="", style_el_line=None):
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
					prev_element_index = index_pile[-1]

					# See if the previous element was defined in the style
					has_custom_style = False
					if style_el_line != prev_element_index:
						for s_index, i in enumerate(style_element_indices):
							if prev_element_index == i:
								has_custom_style = True
								break

					if has_custom_style:
						# This is a custom element, custom attributes apply
						prev_el_attributes = self.style_attributes[style_element_name[s_index]]
						if attribute in prev_el_attributes:
							_element_name = layout_elements[prev_element_index].name
							block_element_name = prev_el_attributes[attribute][1]
							el_name = _element_name + "." + block_element_name
							block_element = layout_elements[layout_table[el_name]-offset]

							# Add attribute
							block_element.setAttribute(prev_el_attributes[attribute][0], attribute_value)
						elif layout_elements[prev_element_index].hasAttribute(attribute):
							# Add the attribute to the block main object if it exists
							layout_elements[prev_element_index].setAttribute(attribute, attribute_value)
						else:
							log(ERROR, attribute + " not part of custom element")
							exit(1)
					else:
						layout_elements[prev_element_index].setAttribute(attribute, attribute_value)
				else:
					root_att[attribute] = attribute_value
			else:
				# Look for new element
				element_type = data[0]
				element_name = prefix + data[1]

				# Parse this new element
				if element_type in EL_TABLE:
					# Regular element
					layout_elements.append(EL_TABLE[element_type](element_name))
				elif element_type in self.style_chunks:
					# Customed defined element
					definition = self.style_chunks[element_type]
					layout_elements.append(EL_TABLE[definition[0]](element_name))
					style_element_indices.append(len(layout_elements)-1)
					style_element_name.append(element_type)
					self.style_element_type[element_name] = element_type
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
				if element_type in self.style_chunks:
					definition = self.style_chunks[element_type]

					for style_line in definition[1:]:
						_loadLineInfo(line_number, style_line, n_lines, off_indent=indent, prefix=element_name + ".", style_el_line=len(layout_elements)-1)

		# Loop through all the lines
		for line_number, line in enumerate(layout_content):
			_loadLineInfo(line_number, line, n_lines_content)

		return layout_elements, layout_tree, layout_table, root_indices, root_att

	def _loadStyle(self, style_file_name):
		style_chunks = {}
		style_attributes = {}

		# TODO organise as a tree
		last_element_name = None

		# Open and read the file
		with open(style_file_name + ".lia", "r") as style_file:
			style_lines = style_file.readlines()
			style_lines.append("\n")

		n_lines = len(style_lines)
		style_element_name = ""

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
				style_element_name = data[1]
				style_chunks[style_element_name] = [data[0]]
				style_attributes[style_element_name] = {}
			else:
				# Test if custom attribute
				if data[0].startswith("!"):
					# What follows the ! is the alias
					full_data = data[1].split(" ", 1)
					indentation = '\t' * indent
					style_chunks[style_element_name].append(indentation + "." + data[1])
					style_attributes[style_element_name][data[0][1:]] = [full_data[0], last_element_name]
				else:
					# Record the last element name
					if not data[0].startswith("."):
						last_element_name = data[1]
					style_chunks[style_element_name].append(line)

		return style_chunks, style_attributes

	def changeElement(self, element_name, attribute, value):
		# This attribute refers to a previous element
		element_index = self.layout_table[element_name]
		element = self.layout_elements[element_index]

		if element_name not in self.style_element_type:
			# Regular element
			element.setAttribute(attribute, value)
		else:
			# Custom element, custom attributes apply
			element_attributes = self.style_attributes[self.style_element_type[element_name]]

			if attribute in element_attributes:
				block_element_name = element_attributes[attribute][1]
				el_name = element_name + "." + block_element_name
				block_element = self.layout_elements[self.layout_table[el_name]]

				# Add attribute
				block_element.setAttribute(element_attributes[attribute][0], value)
			else:
				log(ERROR, attribute + " not part of custom element")
				exit(1)

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
