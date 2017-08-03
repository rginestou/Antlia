class Rect:
	"""
	Bounding box to position the elements in the GUI
	"""
	def __init__(self, x, y, w, h):
		self.x = x; self.y = y
		self.w = w; self.h = h

	def fitRect(self, box_rect):
		"""
		The element's rects are normalized.
		When given a bounding rect, this method scales self to
		fit into the box.
		Assume that all self args are within [0,1]
		"""
		bX = box_rect.x
		bY = box_rect.y
		sX = box_rect.w
		sY = box_rect.h
		return Rect(int(bX + self.x * sX), int(bY + self.y * sY), int(self.w * sX), int(self.h * sY))

	def getTuple(self):
		return (self.x, self.y, self.w, self.h)

	def isOver(self, X, Y):
		return self.x < X < self.x + self.w and\
		 		self.y < Y < self.y + self.h

	def __str__(self):
		return "Rect(" + str(self.x) + ", " + str(self.y) + ", " +\
		 		str(self.w) + ", " + str(self.h) + ")"
