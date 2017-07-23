import json
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
		# Build an array of element with position and size
		self.layout = []

		pprint(self.layout)


	def getHandlers(self):
		return {}

	def getLayout(self):
		return self.layout
