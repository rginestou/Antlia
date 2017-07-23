from sources.parser import Parser
from sources.renderer import Renderer
from sources.message import log, ERROR, WARNING, OK

class Antlia:
	"""The Antlia Class is the only object the user of the library
	has access to. Once instanciated, it is used to manage the
	links between the elements of the GUI and the backend."""
	def __init__(self, layout, style=None):
		self.layout_file_name = layout
		self.style_file_name = style

		# The Parser that will read all informations from both
		# the layout and style files
		self.parser = Parser(self.layout_file_name, self.style_file_name)
		self.handlers = self.parser.getHandlers()
		self.layout = self.parser.getLayout()

		# The Renderer will take a reference to the layout to display it
		self.renderer = Renderer(self.layout)

	def bind(self, element_name, handler):
		"""Binds an element of the GUI with an handler."""
		if element_name in self.handlers:
			self.handlers[element_name] = handler
		else:
			log(WARNING, element_name + " does not exist in the layout")

	def change(self, element_name, parameter, value):
		"""Changes an element's parameter value"""
		pass
