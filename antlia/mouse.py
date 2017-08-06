class Mouse:
	"""the Mouse objects stores the state
	of the mouse."""
	def __init__(self):
		# Buttons
		self.left_click = False
		self.right_click = False

		# Local Positions
		self.X = None
		self.Y = None

		# Global Positions
		self.global_X = None
		self.global_Y = None
