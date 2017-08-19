from .translate import toArrayOfSizes
from ..blueprint.rectangle import Rectangle
from ..message import catch, ERROR, WARNING, OK
from .element import Element
from ..rect import Rect
from .color import Color
from .const import *

class Grid(Element):
	def __init__(self, name):
		super(Grid, self).__init__(name)
		self.type = "grid"

		# Specific to the Grid element
		self.attributes = {
			"rows": "1",
			"cols": "1",
			"drag-window": False,
			"background-color": "none",
			"padding": "0px"
		}

	def placeChildren(self, rect, n_child):
		# Reset children
		self.child_rects = []

		# Apply padding
		grid_rect = rect.getPaddingRect(self.attributes["padding"])

		rows, rows_typ = catch(
			toArrayOfSizes, (self.attributes["rows"], grid_rect.h),
			ERROR, self.name + " .rows")

		cols, cols_typ = catch(
			toArrayOfSizes, (self.attributes["cols"], grid_rect.w),
			ERROR, self.name + " .cols")

		sr = grid_rect.y; sc = grid_rect.x
		for r, row_ in enumerate(rows):
			row = int(row_)
			if rows_typ[r] == "%":
				row = int(row_ * grid_rect.h)
			for c, col_ in enumerate(cols):
				col = int(col_)
				if cols_typ[c] == "%":
					col = int(col_ * grid_rect.w)

				self.child_rects.append(Rect(sc, sr, col, row))
				sc += col
			sr += row
			sc = grid_rect.x

	def build(self, renderer, rect):
		# Fetch colors
		colors = {
			"background": Color[self.attributes["background-color"]]
		}


		### Bluid blueprint ###
		self._clearBlueprint()

		if colors["background"] is not None:
			self._addNewPrimitive(Rectangle, renderer, rect, colors["background"])
