class Color:
	"""
	Used to represent a color
	Component within [0, 255]
	"""
	def __init__(self, r, g, b):
		self.R = r
		self.G = g
		self.B = b

class C:
	blue = Color(53,152,219)
	orange = Color(243,156,17)
	green = Color(14,227,75)
	grey = Color(129,129,129)
	lightgrey = Color(212,212,212)
	darkgrey = Color(86,84,81)
	white = Color(255,255,255)
