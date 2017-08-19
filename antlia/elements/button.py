from .translate import toColor
from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from .element import Element
from .const import *
from .color import Color, lighthen

class Button(Element):
	def __init__(self, name):
		super(Button, self).__init__(name)
		self.type = "button"

		# Specific to the Button element
		self.attributes = {
			"state": "released",
			"label": name,
			"font": "lato-light",
			"text-size": 12,
			"text-color": "white"
			"text-align": "center",
			"released-color": "peter-river",
			"pressed-color": "belize-hole",
			"hovered-color": "peter-river",
			"drag-window": False,
		}

	def build(self, renderer, rect):
		# Fetch colors
		colors = {
			"released":  toColor(self.attributes["released-color"]),
			"pressed": toColor(self.attributes["pressed-color"]),
			"hovered": lighthen(toColor(self.attributes["hovered-color"])),
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

	def onClick(self):
		self.setAttribute("state", "pressed")

	def onRelease(self):
		self.setAttribute("state", "hovered")

	def onHover(self, local_x, local_y):
		self.setAttribute("state", "hovered")

	def onOut(self):
		self.setAttribute("state", "released")
