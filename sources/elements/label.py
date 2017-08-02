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
			"label": "Button",
			"align": "left",
			"background-color": "clouds",
			"text-color": "white",
			"text-size": 12
		}

	def build(self, renderer, rect):
		colors = {
			"background-color": Color[self.attributes["background-color"]],
			"text-color": Color[self.attributes["text-color"]]
		}

		# Bluid blueprint
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
				b"resources/roboto-regular.ttf",
				self.attributes["text-size"],
				align=self.attributes["align"])
		T.build(renderer, rect, colors["text-color"])
		self.blueprint.append(T)
