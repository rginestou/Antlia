from sources.blueprint.blueprint import Blueprint
from sources.blueprint.rectangle import Rectangle
from .element import Element
from .color import C
from .const import *

class Button(Element):
	def __init__(self):
		super(Button, self).__init__()
		# Specific to the Button element
		self.state = RELEASED

		self.colors = {
			"released-color": C.white,
			"pressed-color": C.grey,
			"hovered-color": C.blue,
			"text-color": C.darkgrey
		}

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		R.setColorId("pressed-color")
		self.blueprint.appendPrimitive(R)
