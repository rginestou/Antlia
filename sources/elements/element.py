from sources.message import log, ERROR, WARNING, OK

class Element:
	"""
	The GUI element will derive from this class.
	"""
	def __init__(self, name):
		# Set the name
		self.name = name

		# Specific to the current element
		self.attributes = {}

		# If the element has children, this list will be filled with rects
		self.child_rects = []

		# Set of colors to be used by default by the element
		self.colors = {}

		# List of primitives that defines the visual of the element
		self.blueprint = []

	def build(self):
		"""
		Method to call after all the attributes are setup.
		It will perform operations required for each element
		and finaly build them
		"""
		return

	def draw(self, renderer, rect):
		pass

	def onClick(self):
		pass

	def onRelease(self):
		pass

	def onHover(self):
		pass

	def onOut(self):
		pass

	def setAttribute(self, att, value):
		if att in self.attributes:
			self.attributes[att] = value
		else:
			log(WARNING, att + " is not an attribute of " + self.name)

	def getAttributes(self):
		return self.attributes

	def __str__(self):
		string = "----> " + self.name + "\n"
		for a in self.attributes:
			string += a + ": " + str(self.attributes[a]) + ",\n"
		return string
