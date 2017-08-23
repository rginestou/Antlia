from .translate import toColor
from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from ..rect import Rect
from .element import Element
from .const import *
from .color import Color, lighthen

class Radio(Element):
	def __init__(self, name):
		super(Radio, self).__init__(name)
		self.type = "radio"

		# Specific to the Button element
		self.attributes = {
			"state": "unchecked",
			"label": name,
			"scope": None,
			"font": "lato-light",
			"text-size": 12,
			"box-size": 30,
			"text-color": "white",
			"text-align": "center",
			"unchecked-color": "clouds",
			"checked-color": "peter-river",
		}

	def build(self, renderer, rect):
		# Fetch colors
		colors = {
			"ckecked":  toColor(self.attributes["checked-color"]),
			"unchecked": toColor(self.attributes["unchecked-color"]),
			"text": toColor(self.attributes["text-color"])
		}

		text_size = self.attributes["text-size"]
		box_size = self.attributes["box-size"]
		state = self.attributes["state"]

		text_rect = Rect(rect.x + int(box_size * 1.2), rect.y, rect.w - int(box_size * 1.2), rect.h)

		### Bluid blueprint ###
		self._clearBlueprint()

		if state == "checked":
			icon = "#radio_button_checked#"
			color = colors["ckecked"]
		elif state == "unchecked":
			icon = "#radio_button_unchecked#"
			color = colors["unchecked"]

		self._addNewPrimitive(Text, renderer, rect, color, args=(
			icon,
			self.attributes["font"],
			box_size,
			"left"
		))

		self._addNewPrimitive(Text, renderer, text_rect, colors["text"], args=(
			self.attributes["label"],
			self.attributes["font"],
			text_size,
			"left"
		))

	def onClick(self, local_x, local_y):
		state = self.attributes["state"]
		if state == "checked":
			self.setAttribute("state", "unchecked")
		elif state == "unchecked":
			self.setAttribute("state", "checked")
		return True
