from .translate import toColor
from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from .element import Element
from .const import *
from .color import Color, lighthen

class DropDown(Element):
	def __init__(self, name):
		super(DropDown, self).__init__(name)
		self.type = "drop-down"

		# Specific to the Button element
		self.attributes = {
			"state": "released",
			"rows": "1",
			"label": name,
			"font": "lato-light",
			"text-size": 12,
			"text-color": "white",
			"text-align": "center",
			"released-color": "peter-river",
			"hovered-color": "peter-river",
			"pressed-color": "belize-hole",
			"drop-released-color": "white",
			"drop-hovered-color": "white",
			"drop-pressed-color": "clouds",
			"drag-window": False,
		}

	def placeChildren(self, rect, n_child):
		# Reset children
		self.child_rects = []

		rows, rows_typ = catch(
			toArrayOfSizes, (self.attributes["rows"], rect.h),
			ERROR, self.name + " .rows")

		sr = rect.y
		for r, row_ in enumerate(rows):
			row = int(row_)
			if rows_typ[r] == "%":
				row = int(row_ * grid_rect.h)
			
			self.child_rects.append(Rect(grid_rect.x, sr, grid_rect.w, row))
			sr += row

	def build(self, renderer, rect):
		# Fetch colors
		colors = {
			"released":  toColor(self.attributes["released-color"]),
			"pressed": toColor(self.attributes["pressed-color"]),
			"hovered": lighthen(toColor(self.attributes["hovered-color"])),
			"drop-released":  toColor(self.attributes["drop-released-color"]),
			"drop-pressed": toColor(self.attributes["drop-pressed-color"]),
			"drop-hovered": lighthen(toColor(self.attributes["drop-hovered-color"])),
			"text": toColor(self.attributes["text-color"])
		}

		# Button color based on its state
		button_color = colors[self.attributes["state"]]

		# Position the text using its alignment
		text_align = self.attributes["text-align"]
		x = 0.5
		if text_align == "left":
			x = 0.0
		elif text_align == "right":
			x = 1.0


		### Bluid blueprint ###
		self._clearBlueprint()

		self._addNewPrimitive(Rectangle, renderer, rect, button_color)
		self._addNewPrimitive(Text, renderer, rect, colors["text"], args=(
			self.attributes["label"],
			self.attributes["font"],
			self.attributes["text-size"],
			text_align
		))

	def onClick(self, local_x, local_y):
		self.setAttribute("state", "pressed")
		return True

	def onRelease(self):
		self.setAttribute("state", "hovered")
		return True

	def onHover(self, local_x, local_y):
		self.setAttribute("state", "hovered")
		return True

	def onOut(self):
		self.setAttribute("state", "released")
		return True
