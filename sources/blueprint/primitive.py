class Primitive:
	"""docstring for Primitive."""
	def __init__(self):
		self.vertices = None
		self.color_id = None

	def getVerticies(self):
		return self.vertices

	def getColorId(self):
		return self.color_id

	def setColorId(self, c):
		self.color_id = c
