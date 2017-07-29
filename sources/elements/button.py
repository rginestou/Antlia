from ..blueprint.rectangle import Rectangle
from .element import Element
from .color import C
from .const import *

class Button(Element):
	def __init__(self):
		super(Button, self).__init__()
		# Specific to the Button element
		self.attributes = {
			"state": RELEASED,
			"label": "Button"
		}

		self.colors = {
			"released-color": C.white,
			"pressed-color": C.grey,
			"hovered-color": C.blue,
			"text-color": C.darkgrey
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		self.blueprint.append(R)

	def draw(self, renderer, rect):
		if self.attributes["state"] == RELEASED:
			self.blueprint[0].draw(renderer, rect, self.colors["released-color"])
		elif self.attributes["state"] == HOVERED:
			self.blueprint[0].draw(renderer, rect, self.colors["hovered-color"])
