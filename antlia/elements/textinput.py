from ..blueprint.rectangle import Rectangle
from .translate import toArrayOfSizes
from ..blueprint.text import Text
from ..blueprint.primitive import font_manager
from .element import Element
from .color import Color, lighthen
from ..rect import Rect
from .const import *

class TextInput(Element):
	def __init__(self, name):
		super(TextInput, self).__init__(name)
		self.type = "text-input"

		# Specific to the Button element
		self.attributes = {
			"placeholder": name,
			"label": "",
			"align": "left",
			"background-color": "none",
			"font": "lato-light",
			"text-color": "dark-grey",
			"placeholder-color": "grey",
			"underline-thickness": "2px",
			"underline-color": "peter-river",
			"text-size": 12,
			"character-limit": 40,
			"padding": "0px"
		}

		# State of the input
		self.state = ACTIVE # TODO
		self.cursor_position = 0

	def build(self, renderer, rect):
		self._clearBlueprint()
		colors = {
			"background-color": Color[self.attributes["background-color"]],
			"text-color": Color[self.attributes["text-color"]],
			"placeholder-color": Color[self.attributes["placeholder-color"]],
			"underline-color": Color[self.attributes["underline-color"]]
		}

		# Apply padding
		text_rect = rect.getPaddingRect(self.attributes["padding"])

		text_size = int(self.attributes["text-size"])
		character_limit = int(self.attributes["character-limit"])

		# Bluid background
		if colors["background-color"] is not None:
			R = Rectangle(0.0, 0.0, 1.0, 1.0)
			R.build(renderer, rect, colors["background-color"])
			self.blueprint.append(R)

		# Underline
		U = Rectangle(0.0, 0.0, 1.0, 1.0)
		t, _, _  = toArrayOfSizes(self.attributes["underline-thickness"], rect.h)
		thickness = t[0]
		r = Rect(rect.x, rect.y + rect.h/2+text_size*0.7 - thickness, rect.w, thickness)
		U.build(renderer, r, colors["underline-color"])
		self.blueprint.append(U)

		# Text
		text_color = colors["text-color"]
		text = self.attributes["label"]
		if text == "":
			text_color = colors["placeholder-color"]
			text = self.attributes["placeholder"]

		x = 0.0
		if self.attributes["align"] == "center":
			x = 0.5
		elif self.attributes["align"] == "right":
			x = 1.0

		T = Text(x, 0.5,
				text,
				self.attributes["font"],
				text_size,
				align=self.attributes["align"])
		T.build(renderer, text_rect, text_color)
		self.blueprint.append(T)

	def onHover(self, local_x, local_y):
		print(local_x, local_y)
		# print(font_manager.getGlyphFromChar(T.getFontId(), "H").advance)

	def onTextInput(self, text):
		character_limit = int(self.attributes["character-limit"])
		if self.state == ACTIVE:
			# Special character
			if text == "BACKSPACE":
				self.attributes["label"] = self.attributes["label"][:-1]
			elif len(self.attributes["label"]) < character_limit:
				# Add text to the label
				self.cursor_position
				self.attributes["label"] += text
			return True
		return False
