from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from ..blueprint.primitive import font_manager
from .element import Element
from .color import Color, lighthen
from .const import *

class Label(Element):
	def __init__(self, name):
		super(Label, self).__init__(name)
		self.type = "label"

		# Specific to the Button element
		self.attributes = {
			"label": name,
			"drag-window": False,
			"background-color": "none",
			"font": "lato-light",
			"text-color": "dark-grey",
			"text-align": "left",
			"text-size": 12,
			"padding": "0px"
		}

	def build(self, renderer, rect):
		# Apply padding
		text_rect = rect.getPaddingRect(self.attributes["padding"])

		# Fetch colors
		colors = {
			"background-color": Color[self.attributes["background-color"]],
			"text-color": Color[self.attributes["text-color"]]
		}

		# Position the text using its alignment
		text_align = self.attributes["text-align"]
		x = 0.5
		if text_align == "left":
			x = 0.0
		elif text_align == "right":
			x = 1.0


		### Bluid blueprint ###
		self._clearBlueprint()

		if colors["background-color"] is not None:
			self._addNewPrimitive(Rectangle, renderer, rect, colors["background-color"])

		self._addNewPrimitive(Text, renderer, text_rect, colors["text-color"], args=(
			self.attributes["label"],
			self.attributes["font"],
			self.attributes["text-size"],
			text_align
		))
