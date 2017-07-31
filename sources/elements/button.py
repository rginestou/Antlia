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
			"label": "Button"
		}

		self.colors = {
			"released-color": Color["peter_river"],
			"pressed-color": Color["belize_hole"],
			"hovered-color": lighthen(Color["peter_river"]),
			"text-color": Color["white"]
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		self.blueprint.append(R)
		T = Text(0.5, 0.5, "Button", b"resources/roboto-reg.ttf", Color["white"], align="center")
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
