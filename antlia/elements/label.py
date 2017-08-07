from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from .element import Element
from .color import Color, lighthen
from .const import *

class Label(Element):
	def __init__(self, name):
		super(Label, self).__init__(name)
		# Specific to the Button element
		self.attributes = {
			"label": name,
			"align": "left",
			"drag-window": False,
			"background-color": "none",
			"font": "lato-light",
			"text-color": "white",
			"text-size": 12,
			"padding": "0px"
		}

	def build(self, renderer, rect):
		self._clearBlueprint()
		colors = {
			"background-color": Color[self.attributes["background-color"]],
			"text-color": Color[self.attributes["text-color"]]
		}

		# Apply padding
		text_rect = rect.getPaddingRect(self.attributes["padding"])

		# Bluid blueprint
		if colors["background-color"] is not None:
			R = Rectangle(0.0, 0.0, 1.0, 1.0)
			R.build(renderer, rect, colors["background-color"])
			self.blueprint.append(R)

		x = 0.0
		if self.attributes["align"] == "center":
			x = 0.5
		elif self.attributes["align"] == "right":
			x = 1.0
		T = Text(x, 0.5,
				self.attributes["label"],
				self.attributes["font"],
				self.attributes["text-size"],
				align=self.attributes["align"])

		T.build(renderer, text_rect, colors["text-color"])
		self.blueprint.append(T)
