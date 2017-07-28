import json
import copy
import os.path
from sources.message import log, ERROR, WARNING, OK
from pprint import pprint

class Parser:
	"""
	The Parser reads the layout and style files and builds
	an array of elements to be displayed in the GUI, taking
	into account the style given by the user.
	"""
	def __init__(self, layout_file_name, style):
		self.style_file_name = style

		# Check if layout file exists
		if not os.path.exists(layout_file_name + ".lia"):
			log(ERROR, "Layout file does not exist", "Import a valid .lia file")
			exit(1)

		self.layout = {
			"parameters": {
				"resolution": {"width": 800, "height": 400}
			},
			"layout": [
				{
					"type": "grid",
					"name": "main_grid",
					"parameters": {
						"rows": [40, 30, 30],
						"cols": 1
					},
					"layout": [
						[
							{
								"type": "custom_button",
								"name": "hello_button"
							}
						],
						[
							{
								"type": "custom_label",
								"name": "hello_label"
							}
						],
						[]
					]
				}
			]
		}
		# self._loadTemplate(layout_file_name)

		# Transform the user defined layout in array of elements
		self._buildLayout()

	def _buildLayout(self):
		"""
		Build an array of element with absolute position, size and other parameters
		"""
		self.layout_struct = [{
			"name": "Untitled window",
			"resolution": {"width": 800, "height": 400},
			"fullscreen": False
		}]
		# self.layout_struct.append(self._loadTemplate("templates/window", self.user_layout["parameters"]))

		pprint(self.layout_struct)

	def _loadTemplate(self, template_name, user_template={}):
		"""
		Load the full default template and customize it with the user defined props
		recursively using the layout file specified
		"""

		# Open and read the file
		with open(template_name + ".lia", "r") as template_file:
			lines = template_file.readlines()

		# Build the layout recursively
		prev = None
		i = 0
		n_lines = len(lines)
		def _aux(prev_indent, obj):
			# Don't go too far
			if i > n_lines:
				return obj

			# Get data
			indent, data = self._parseLine(lines[i])

			# If line empty, go to next
			if len(data) == 0:
				i += 1
				_aux(prev_indent, obj)

			# Process data
			# TODO

		# Get the full layout
		layout = _aux(0, {})

		# TODO
		for prop in user_template:
			try:
				template[prop] = user_template[prop]
			except KeyError:
				log(WARNING, prop + " is not a valid property", "")


		return layout

	def _parseLine(self, line):
		indent = 0
		while line[indent] == "\t":
			indent += 1
		return indent, line.replace("\t", "").replace("\n", "").split(" ")

	def getHandlers(self):
		return {}

	def getLayoutStruct(self):
		return self.layout_struct
