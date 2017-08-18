from ..message import log, ERROR, WARNING, OK

class Element:
	"""
	The GUI element will derive from this class.
	"""
	def __init__(self, name):
		# Set the name
		self.name = name
		self.type = "none"

		# Specific to the current element
		self.attributes = {}

		# If the element has children, this list will be filled with rects
		self.child_rects = []

		# Set of colors to be used by default by the element
		self.colors = {}

		# List of primitives that defines the visual of the element
		self.blueprint = []

	def build(self, renderer, rect):
		"""
		Method to call after all the attributes are setup.
		It will perform operations required for each element
		and finaly build them
		"""
		pass

	def placeChildren(self, rect, n_child):
		"""
		The elements that have children will compute their rects
		"""
		pass

	def _clearBlueprint(self):
		# Clear previous primitives
		for p in self.blueprint:
			p.destroy()
		self.blueprint = []

	def _addNewPrimitive(self, primitive, renderer, rect, colors, args=None):
		if args is None:
			new_prim = primitive()
		else:
			new_prim = primitive(*args)
		new_prim.build(renderer, rect, colors)
		self.blueprint.append(new_prim)

	def draw(self, renderer):
		for e in self.blueprint: e.draw(renderer)

	def onClick(self):
		pass

	def onRelease(self):
		pass

	def onHover(self, local_x, local_y):
		pass

	def onOut(self):
		pass

	def onTextInput(self, text):
		return False

	def setAttribute(self, att, value):
		"""
		Set a particular attribute to a new value.
		A translation if performed if the default type differs from
		the value
		"""
		if att in self.attributes:
			self.attributes[att] = value
		else:
			log(WARNING, att + " is not an attribute of " + self.name)

	def hasAttribute(self, att):
		return att in self.attributes

	def getAttributes(self):
		return self.attributes

	def getAttribute(self, att):
		if att in self.attributes:
			return self.attributes[att]
		else:
			return None

	def __str__(self):
		string = "----> " + self.name + "\n"
		for a in self.attributes:
			string += a + ": " + str(self.attributes[a]) + ",\n"
		return string
