from .translate import toArrayOfSizes
from ..blueprint.rectangle import Rectangle
from ..message import log, ERROR, WARNING, OK
from .element import Element
from ..rect import Rect
from .color import Color
from .const import *

class Grid(Element):
	def __init__(self, name):
		super(Grid, self).__init__(name)
		# Specific to the Grid element
		self.attributes = {
			"rows": "1",
			"cols": "1",
			"drag-window": False,
			"background-color": "none",
			"padding": "0px"
		}

	def placeChildren(self, rect, n_child):
		# Apply padding
		grid_rect = rect.getPaddingRect(self.attributes["padding"])

		# Create rects based on the rows and columns proportions
		s = 0.0

		rows, rows_typ, err = toArrayOfSizes(self.attributes["rows"], grid_rect.h)
		if err is not None:
			log(ERROR, self.name + " .rows:" + err)
			exit(1)
		cols, cols_typ, err = toArrayOfSizes(self.attributes["cols"], grid_rect.w)
		if err is not None:
			log(ERROR, self.name + " .cols: " + err)
			exit(1)

		sr = grid_rect.y; sc = grid_rect.x
		for r, row_ in enumerate(rows):
			row = row_
			if rows_typ[r] == "%":
				row = row_ * grid_rect.h
			for c, col_ in enumerate(cols):
				col = col_
				if cols_typ[c] == "%":
					col = col_ * grid_rect.w

				self.child_rects.append(Rect(sc, sr, col, row))
				sc += col
			sr += row
			sc = grid_rect.x

	def build(self, renderer, rect):
		self._clearBlueprint()

		colors = {
			"background-color": Color[self.attributes["background-color"]]
		}

		# Bluid blueprint
		if colors["background-color"] is not None:
			R = Rectangle(0.0, 0.0, 1.0, 1.0)
			R.build(renderer, rect, colors["background-color"])
			self.blueprint.append(R)
