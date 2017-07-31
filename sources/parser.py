import json
import copy
import os.path
from sources.message import log, ERROR, WARNING, OK
from .elements.color import Color
from .elements.const import *
from .elements.table import EL_TABLE
from pprint import pprint

# Elements
from sources.elements.window import Window
from sources.elements.grid import Grid
from sources.elements.button import Button

class Parser:
	"""
	The Parser reads the layout and style files and builds
	an array of elements to be displayed in the GUI, taking
	into account the style given by the user.
	"""
	def __init__(self, layout_file_name, style_file_name):
		self.style_file_name = style_file_name

		# Check if layout file exists
		if not os.path.exists(layout_file_name + ".lia"):
			log(ERROR, "Layout file does not exist", "Import a valid .lia file")
			exit(1)

		# Transform the user defined layout in array of elements
		self._buildLayout(layout_file_name)

	def _buildLayout(self, layout_file_name):
		"""
		Build an array of element and their rects
		"""
		w = Window("window")

		self.layout_elements, self.layout_tree, self.layout_table = self._loadTemplate(layout_file_name)

	def _loadTemplate(self, template_name):
		"""
		Load the full default template and customize it with the user defined props
		recursively using the layout file specified
		"""
		# Declare the layout variables
		layout_elements = [Window("window")]
		layout_tree = [[]]
		layout_table = {
			"window": 0
		}

		# Open and read the file
		with open(template_name + ".lia", "r") as template_file:
			index_pile = [0]
			element_indent = -1
			n_element = 1
			for line in template_file:
				# Get data
				indent, data = self._parseLine(line)

				# Jump to next line if empty
				if len(data) == 0 or data[0] == "":
					continue

				# print(data, layout_tree, index_pile)

				# Look for indentation
				i = indent
				while i <= element_indent:
					child_index = index_pile[-1]
					layout_elements[child_index].settle()
					index_pile.pop()
					layout_tree[index_pile[-1]].append(child_index)
					i += 1

				if data[0][0] == ".":
					# Parse properties (start with .)
					new_att = data[1:]
					if len(new_att) == 1:
						new_att = new_att[0]
					layout_elements[index_pile[-1]].setAttribute(data[0][1:], new_att)
					continue
				else:
					# Parse new element
					layout_elements.append(EL_TABLE[data[0]](data[1]))
					layout_tree.append([])
					layout_table[data[1]] = n_element
					element_indent = indent

					# Add to the pile
					index_pile.append(n_element)

					n_element += 1

			# Process the remaining items in the pile
			i = 0
			while i <= element_indent:
				child_index = index_pile[-1]
				layout_elements[child_index].settle()
				index_pile.pop()
				layout_tree[index_pile[-1]].append(child_index)
				i += 1

		return layout_elements, layout_tree, layout_table

	def _parseLine(self, line):
		indent = 0
		while line[indent] == "\t":
			indent += 1
		return indent, line.replace("\t", "").replace("\n", "").split(" ")

	def getHandlers(self):
		return {}

	def getLayoutElements(self):
		return self.layout_elements

	def getLayoutTree(self):
		return self.layout_tree

	def getLayoutTable(self):
		return self.layout_table
