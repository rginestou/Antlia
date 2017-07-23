import numpy

class Builder(object):
	"""
	The Builder takes the GUI layout as a JSON file and
	will produce a vertex array understandable by openGL
	"""
	def __init__(self):
		pass

	def getLayoutData(self, layout_struct):
		"""

		"""

		return numpy.array([
			 # X,    Y,    Z     R,   G,   B,   A
			 0.0,  0.0,  0.0,  1.0, 0.0, 0.0, 1.0,
			 1.0,  0.0,  0.0,  1.0, 0.0, 0.0, 1.0,
			 0.0,  1.0,  0.0,  1.0, 0.0, 0.0, 1.0,
			 1.0,  0.0,  0.0,  1.0, 0.0, 0.0, 1.0,
			 0.0,  1.0,  0.0,  1.0, 0.0, 0.0, 1.0,
			 1.0,  1.0,  0.0,  1.0, 0.0, 0.0, 1.0,
		], dtype=numpy.float32)
