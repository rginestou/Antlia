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

		with open(layout_file_name + ".lia", "r") as layout_file:
			self.user_layout = json.load(layout_file)

		# Transform the user defined layout in array of elements
		self._buildLayout()

	def _buildLayout(self):
		"""
		Build an array of element with absolute position, size and other parameters
		recursively using the layout file specified
		"""
		self.layout_struct = []
		self.layout_struct.append(self._loadTemplate("window", self.user_layout["parameters"]))

		pprint(self.layout_struct)

	def _loadTemplate(self, template_name, user_template):
		"""
		Load the full default template and customize it with the user defined props
		"""
		with open("templates/" + template_name + ".lia", "r") as template_file:
			template = json.load(template_file)

		for prop in user_template:
			try:
				template[prop] = user_template[prop]
			except KeyError:
				log(WARNING, prop + " is not a valid property", "")

		return template

	def getHandlers(self):
		return {}

	def getLayoutStruct(self):
		return self.layout_struct
