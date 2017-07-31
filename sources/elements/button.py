from ..blueprint.rectangle import Rectangle
from .element import Element
from .color import C
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
			"released-color": C.lightergrey,
			"pressed-color": C.blue,
			"hovered-color": C.lightgrey,
			"text-color": C.white
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		self.blueprint.append(R)

	def draw(self, renderer, rect):
		if self.attributes["state"] == RELEASED:
			self.blueprint[0].draw(renderer, rect, self.colors["released-color"])
		elif self.attributes["state"] == HOVERED:
			self.blueprint[0].draw(renderer, rect, self.colors["hovered-color"])
		elif self.attributes["state"] == PRESSED:
			self.blueprint[0].draw(renderer, rect, self.colors["pressed-color"])

	def onClick(self):
		self.setAttribute("state", PRESSED)

	def onRelease(self):
		self.setAttribute("state", HOVERED)

	def onHover(self):
		self.setAttribute("state", HOVERED)

	def onOut(self):
		self.setAttribute("state", RELEASED)
