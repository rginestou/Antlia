class Blueprint:
	"""
	Define the construction of the graphical
	part of a GUI element.
	A blueprint is composed of primitives whose
	proportions and positions are to be defined.
	"""
	def __init__(self):
		self.primitives = []

	def getPrimitives(self):
		return self.primitives

	def appendPrimitive(self, P):
		self.primitives.append(P)
