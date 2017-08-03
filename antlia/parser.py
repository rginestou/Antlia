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

		# Transform the user defined layout in array of elements
		self._buildLayout(layout_file_name, style_file_name)

	def _buildLayout(self, layout_file_name, style_file_name):
		"""
		Build an array of element and their rects
		"""
		layout_elements, layout_tree, layout_table, root_indices, root_att = self._loadTemplate(layout_file_name, offset=1)

		# Add the window object
		window = Window("window")
		for a in root_att:
			window.setAttribute(a, root_att[a])
		window.placeChildren()

		self.layout_elements = [window] + layout_elements
		self.layout_tree = [root_indices] + layout_tree
		self.layout_table = layout_table
		self.layout_table["window"] = 0

		# print(self.layout_elements, "\n")
		# print(self.layout_tree, "\n")
		# print(self.layout_table, "\n")

	def _loadTemplate(self, template_name, style_elements=[], style_tree=[], style_table={}, offset=0):
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

		# Open and read the file
		with open(template_name + ".lia", "r") as template_file:
			template_lines = template_file.readlines()
			template_lines.append("\n")

		index_pile = []
		last_element_indent = -1
		n_element = offset
		n_lines = len(template_lines)

		for line_number, line in enumerate(template_lines):
			# Get indent and data of the line
			indent, data = self._parseLine(line)

			if line_number != n_lines-1:
				# Jump to next line if empty or if it is a comment
				if len(data) == 0 or data[0] == "" or data[0][0] == "#":
					line_number += 1
					continue

				# Check if the data contains two blocks
				if len(data) != 2:
					log(ERROR, "Syntax error at line " + str(line_number+1))
					exit(1)

			# Look for indentation differentials
			while last_element_indent >= indent:
				# Fetch last element
				last_element_index = index_pile[-1]

				# This last element is fully setup
				layout_elements[last_element_index].placeChildren()
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
				continue

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
					layout_elements.append(EL_TABLE[element_type](element_name))

				layout_tree.append([])
				layout_table[element_name] = n_element
				last_element_indent = indent

				# Add its index to the pile
				index_pile.append(n_element - offset)

				n_element += 1

		return layout_elements, layout_tree, layout_table, root_indices, root_att

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
