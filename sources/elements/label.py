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
			"align": "left"
		}

		self.colors = {
			"background-color": Color["clouds"],
			"text-color": Color["dark_grey"]
		}

	def build(self):
		self.blueprint = []

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		self.blueprint.append(R)
		x = 0.0
		if self.attributes["align"] == "center":
			x = 0.5
		elif self.attributes["align"] == "right":
			x = 1.0
		T = Text(x, 0.5,
				self.attributes["label"],
				b"resources/roboto-reg.ttf",
				self.colors["text-color"],
				align=self.attributes["align"])
		self.blueprint.append(T)

	def draw(self, renderer, rect):
		self.blueprint[0].draw(renderer, rect, self.colors["background-color"])
		self.blueprint[1].draw(renderer, rect, self.colors["text-color"])
