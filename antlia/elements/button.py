from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from .element import Element
from .color import Color, lighthen
from .const import *

class Button(Element):
	def __init__(self, name):
		super(Button, self).__init__(name)
		# Specific to the Button element
		self.attributes = {
			"state": RELEASED,
			"label": "Button",
			"text-align": "center",
			"text-size": 12,
			"released-color": "peter-river",
			"pressed-color": "belize-hole",
			"hovered-color": "peter-river",
			"text-color": "white"
		}

	def build(self, renderer, rect):
		# Fetch colors
		colors = {
			"released-color": Color[self.attributes["released-color"]],
			"pressed-color": Color[self.attributes["pressed-color"]],
			"hovered-color": lighthen(Color[self.attributes["hovered-color"]]),
			"text-color": Color[self.attributes["text-color"]]
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		color = None
		if self.attributes["state"] == RELEASED:
			color = colors["released-color"]
		elif self.attributes["state"] == HOVERED:
			color = colors["hovered-color"]
		elif self.attributes["state"] == PRESSED:
			color = colors["pressed-color"]
		R.build(renderer, rect, color)
		self.blueprint.append(R)

		x = 0.5
		if self.attributes["text-align"] == "left":
			x = 0.0
		elif self.attributes["text-align"] == "right":
			x = 1.0
		T = Text(x, 0.5,
				self.attributes["label"],
				b"resources/lato-regular.ttf",
				self.attributes["text-size"],
				self.attributes["text-align"])
		T.build(renderer, rect, colors["text-color"])
		self.blueprint.append(T)

	def onClick(self):
		self.setAttribute("state", PRESSED)

	def onRelease(self):
		self.setAttribute("state", HOVERED)

	def onHover(self):
		self.setAttribute("state", HOVERED)

	def onOut(self):
		self.setAttribute("state", RELEASED)
