from .message import catch, ERROR, WARNING, OK
from .elements.translate import toArrayOfSizes

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

	def getPaddingRect(self, padding):
		"""
		Return the rect resulting of the application
		of a padding on the self rect.
		All possible input values are treated.
		"""
		pad_val, pad_typ = catch(
			toArrayOfSizes, (padding,),
			ERROR, ".padding")

		if len(pad_val) == 1:
			# Apply to all direction
			typ = [pad_typ[0], pad_typ[0], pad_typ[0], pad_typ[0]]
			pad = [pad_val[0], pad_val[0], pad_val[0], pad_val[0]]
		elif len(pad_val) == 2:
			# top-bottom, right-left
			typ = [pad_typ[0], pad_typ[1], pad_typ[0], pad_typ[1]]
			pad = [pad_val[0], pad_val[1], pad_val[0], pad_val[1]]
		elif len(pad_val) == 3:
			# top, right-left, bottom
			typ = [pad_typ[0], pad_typ[1], pad_typ[2], pad_typ[0]]
			pad = [pad_val[0], pad_val[1], pad_val[2], pad_val[1]]
		elif len(pad_val) == 4:
			# top, right, bottom, left
			typ = pad_typ
			pad = pad_val
		else:
			return None, "Too many arguments supplied"

		# Convert to px
		pad_px = []
		for i in range(4):
			if typ[i] == "px":
				pad_px.append(pad[i])
			else:
				if i % 2 == 0:
					pad_px.append(self.h * pad[i])
				else:
					pad_px.append(self.w * pad[i])

		# Compute the final Rect
		x = pad_px[1]
		y = pad_px[0]
		h = self.h - pad_px[0] - pad_px[2]
		w = self.w - pad_px[1] - pad_px[3]

		return Rect(int(self.x + x), int(self.y) + y, int(w), int(h))

	def getTuple(self):
		return (self.x, self.y, self.w, self.h)

	def isOver(self, X, Y):
		return self.x < X < self.x + self.w and\
		 		self.y < Y < self.y + self.h

	def __str__(self):
		return "Rect(" + str(self.x) + ", " + str(self.y) + ", " +\
		 		str(self.w) + ", " + str(self.h) + ")"
