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
			"rows": [0.5, 0.5],
			"cols": [1.0]
		}

		self.colors = {
			"background-color": Color["peter_river"]
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		self.blueprint.append(R)

	def settle(self):
		# Create rects based on the rows and columns proportions
		s = 0.0

		# TODO
		if type(self.attributes["rows"]) != list:
			self.attributes["rows"] = [self.attributes["rows"]]
		if type(self.attributes["cols"]) != list:
			self.attributes["cols"] = [self.attributes["cols"]]
		rows = list(map(float, self.attributes["rows"]))
		cols = list(map(float, self.attributes["cols"]))

		sr = 0.0; sc = 0.0
		for r in rows:
			for c in cols:
				self.child_rects.append(Rect(sc, sr, c, r))
				sc += c
			sr += r
			sc = 0.0

	def draw(self, renderer, rect):
		self.blueprint[0].draw(renderer, rect, self.colors["background-color"])
