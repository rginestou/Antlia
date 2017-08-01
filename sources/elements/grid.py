from .translate import toArrayOfSizes
from ..blueprint.rectangle import Rectangle
from .element import Element
from ..rect import Rect
from .color import Color
from .const import *

class Grid(Element):
	def __init__(self, name):
		super(Grid, self).__init__(name)
		# Specific to the Grid element
		self.attributes = {
			"rows": "100%",
			"cols": "100%",
			"background-color": "none"
		}

	def placeChildren(self):
		# Create rects based on the rows and columns proportions
		s = 0.0

		rows, _ = toArrayOfSizes(self.attributes["rows"])
		cols, _ = toArrayOfSizes(self.attributes["cols"])

		sr = 0.0; sc = 0.0
		for r in rows:
			for c in cols:
				self.child_rects.append(Rect(sc, sr, c, r))
				sc += c
			sr += r
			sc = 0.0

	def build(self, renderer, rect):
		colors = {
			"background-color": Color[self.attributes["background-color"]]
		}

		# Bluid blueprint
		if colors["background-color"] is not None:
			R = Rectangle(0.0, 0.0, 1.0, 1.0)
			R.build(renderer, rect, colors["background-color"])
			self.blueprint.append(R)
