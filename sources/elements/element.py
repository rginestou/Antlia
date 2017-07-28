from ..blueprint.blueprint import Blueprint

class Element:
	"""
	The GUI element will derive from this class.
	"""
	def __init__(self):
		# Set of colors to be used by default by the element
		self.colors = {}

		# Blueprint that defines the visual of the element
		self.blueprint = Blueprint()

		# The text to be displayed
		self.texts = []

	def getBlueprintPrimitives(self):
		return self.blueprint.getPrimitives()

	def getColors(self):
		return self.colors
