from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from ..blueprint.primitive import font_manager
from .element import Element
from .color import Color, lighthen
from .const import *

class TextInput(Element):
	def __init__(self, name):
		self.type = "text-input"
		super(TextInput, self).__init__(name)
		# Specific to the Button element
		self.attributes = {
			"placeholder": name,
			"align": "left",
			"background-color": "none",
			"font": "lato-light",
			"text-color": "white",
			"text-size": 12,
			"padding": "0px"
		}

		# State of the input
		self.state = ACTIVE # TODO

	def build(self, renderer, rect):
		self._clearBlueprint()
		colors = {
			"background-color": Color[self.attributes["background-color"]],
			"text-color": Color[self.attributes["text-color"]]
		}

		# Apply padding
		text_rect = rect.getPaddingRect(self.attributes["padding"])

		# Bluid blueprint
		if colors["background-color"] is not None:
			R = Rectangle(0.0, 0.0, 1.0, 1.0)
			R.build(renderer, rect, colors["background-color"])
			self.blueprint.append(R)

		x = 0.0
		if self.attributes["align"] == "center":
			x = 0.5
		elif self.attributes["align"] == "right":
			x = 1.0
		T = Text(x, 0.5,
				self.attributes["label"],
				self.attributes["font"],
				self.attributes["text-size"],
				align=self.attributes["align"])
		T.build(renderer, text_rect, colors["text-color"])
		self.blueprint.append(T)

	def onHover(self, local_x, local_y):
		print(local_x, local_y)
		print(font_manager.getGlyphFromChar(T.getFontId(), "H").advance)

	def onTextInput(self, text):
		if self.state == ACTIVE:
			print(text)
