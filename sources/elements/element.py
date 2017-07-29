class Element:
	"""
	The GUI element will derive from this class.
	"""
	def __init__(self):
		# Specific to the current element
		self.attributes = {}

		# If the element has children, this list will be filled with rects
		self.child_rects = []

		# Set of colors to be used by default by the element
		self.colors = {}

		# List of primitives that defines the visual of the element
		self.blueprint = []

	def settle(self):
		"""
		Method to call after all the attributes are setup.
		It will perform operations required for each element
		"""
		return

	def draw(self, renderer, rect):
		pass

	def setAttribute(self, att, value):
		self.attributes[att] = value

	def getAttributes(self):
		return self.attributes
