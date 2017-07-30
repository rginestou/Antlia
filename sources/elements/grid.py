from ..blueprint.rectangle import Rectangle
from .element import Element
from ..rect import Rect
from .color import C
from .const import *

class Grid(Element):
	def __init__(self, name):
		super(Grid, self).__init__(name)
		# Specific to the Grid element
		self.attributes = {
			"alignment": VERTICAL,
			"proportions": [0.5, 0.5]
		}

		self.colors = {
			"background-color": C.blue
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		self.blueprint.append(R)

	def settle(self):
		# Create rects based on the proportions and alignment
		s = 0.0
		for p in self.attributes["proportions"]:
			if self.attributes["alignment"] == VERTICAL:
				r = Rect(0.0, s, 1.0, p)
			elif self.attributes["alignment"] == HORIZONTAL:
				r = Rect(s, 0.0, p, 1.0)
			s += p
			self.child_rects.append(r)

	def draw(self, renderer, rect):
		self.blueprint[0].draw(renderer, rect, self.colors["background-color"])
