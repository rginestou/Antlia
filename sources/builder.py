import numpy
from sources.elements.button import Button

class Rect:
	def __init__(self, x, y, w, h):
		self.x = x; self.y = y
		self.w = w; self.h = h

class Builder(object):
	"""
	The Builder takes the GUI layout as a tree and
	will produce a vertex array understandable by openGL
	"""
	def __init__(self):
		pass

	def computeLayoutData(self, layout_elements, layout_tree):
		"""
		Given a layout tree of elements, returns the corresponding array of
		triangles and colors to display the GUI (absolute position).
		The given elements have a parenting relation described by the tree,
		and a relative positionning.
		"""

		layout_elements = [Button(), Button()]

		layout_tree = [[], []]

		# Each data chunk is ordered this way :
		# X,	Y,    Z,	R,	G,	B,	A
		layout = []

		def _aux(subtree, rect):
			for node in subtree:
				if len(node) > 0:
					# This is not a leaf
					_aux(node, )

		_aux(layout_tree, Rect(0, 0, 800, 400))


		# Each element has its verticies written in absolute coordinates
		# in the layout buffer
		for el in l:
			layout += self._relativeToAbsolute(el, Rect(0, 0, 400, 400))

		return numpy.array(layout, dtype=numpy.float32)

	def _relativeToAbsolute(self, element, rect):
		"""
		Given a GUI element, break it down to vertices
		and build an array of absolute coordonates out of it.
		"""
		absolute_coord = []
		prim_list = element.getBlueprintPrimitives()
		color_list = element.getColors()
		for p in prim_list:
			c = color_list[p.getColorId()]
			for v in p.getVerticies():
				# Each vertex transforms with respect to its limiting attributes
				X = v.x * rect.w + rect.x
				Y = v.y * rect.h + rect.y

				cv = [X, Y, 0.0, c.R/255.0, c.G/255.0, c.B/255.0, 1.0]
				absolute_coord += cv

		return absolute_coord
