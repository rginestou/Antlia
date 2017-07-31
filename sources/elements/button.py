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
			"align": "center",
			"released-color": "peter_river",
			"pressed-color": "belize_hole",
			"hovered-color": "peter_river",
			"text-color": "white"
		}

	def build(self):
		self.blueprint = []

		# Fetch colors
		self.colors = {
			"released-color": Color[self.attributes["released-color"]],
			"pressed-color": Color[self.attributes["pressed-color"]],
			"hovered-color": lighthen(Color[self.attributes["hovered-color"]]),
			"text-color": Color[self.attributes["text-color"]]
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		self.blueprint.append(R)
		x = 0.5
		if self.attributes["align"] == "left":
			x = 0.0
		elif self.attributes["align"] == "right":
			x = 1.0
		T = Text(x, 0.5,
				self.attributes["label"],
				b"resources/roboto-reg.ttf",
				self.colors["text-color"],
				self.attributes["align"])
		self.blueprint.append(T)

	def draw(self, renderer, rect):
		if self.attributes["state"] == RELEASED:
			self.blueprint[0].draw(renderer, rect, self.colors["released-color"])
		elif self.attributes["state"] == HOVERED:
			self.blueprint[0].draw(renderer, rect, self.colors["hovered-color"])
		elif self.attributes["state"] == PRESSED:
			self.blueprint[0].draw(renderer, rect, self.colors["pressed-color"])
		self.blueprint[1].draw(renderer, rect, self.colors["text-color"])

	def onClick(self):
		self.setAttribute("state", PRESSED)

	def onRelease(self):
		self.setAttribute("state", HOVERED)

	def onHover(self):
		self.setAttribute("state", HOVERED)

	def onOut(self):
		self.setAttribute("state", RELEASED)
