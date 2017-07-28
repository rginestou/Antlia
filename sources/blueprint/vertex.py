class Vertex:
	"""
	Every primitive is made of vertices.
	This vertices have various positionning options,
	giving full control over the primitive positionning.
	"""
	def __init__(self, x, y, minx=0, miny=0, fixed=False):
		self.x = x
		self.y = y
		self.minx = minx
		self.miny = miny
		self.fixed = fixed
