from ..message import catch, ERROR, WARNING, OK
from .translate import toArrayOfSizes
from ..blueprint.rectangle import Rectangle
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
		self.state = INACTIVE
		self.cursor_position = 0
		self.is_hovered = False
		self.cursor_local_x = None

	def build(self, renderer, rect):
		# Apply padding
		text_rect = rect.getPaddingRect(self.attributes["padding"])

		# Fetch colors
		colors = {
			"background": Color[self.attributes["background-color"]],
			"text": Color[self.attributes["text-color"]],
			"placeholder": Color[self.attributes["placeholder-color"]],
			"underline": Color[self.attributes["underline-color"]]
		}

		text_size = int(self.attributes["text-size"])
		character_limit = int(self.attributes["character-limit"])
		t, _ = catch(
			toArrayOfSizes, (self.attributes["underline-thickness"], rect.h),
			ERROR, self.name + " .rows:")
		thickness = t[0]
		underline_rect = Rect(rect.x, int(rect.y + rect.h/2 + text_size*0.7 - thickness), rect.w, thickness)

		text_align = self.attributes["align"]
		text = self.attributes["label"]
		text_color = colors["text"]
		if text == "":
			text_color = colors["placeholder"]
			text = self.attributes["placeholder"]


		### Bluid blueprint ###
		self._clearBlueprint()

		if colors["background"] is not None:
			self._addNewPrimitive(Rectangle, renderer, rect, colors["background"])

		# Underline
		self._addNewPrimitive(Rectangle, renderer, underline_rect, colors["underline"])

		# Text
		text_prim =\
		self._addNewPrimitive(Text, renderer, text_rect, text_color, args=(
			text,
			self.attributes["font"],
			text_size,
			text_align
		))

		# Compute cursor position based on glyphs length
		if self.state == ACTIVE:
			x_displacement = text_rect.x
			y_position = int(text_rect.y + text_rect.h / 2 - text_size * 0.6)
			if self.attributes["label"] != "":
				if self.cursor_local_x is not None:
					# Determine cursor character position
					print(x_displacement, self.cursor_local_x + rect.x)
					p = 0
					for c in text:
						next_displacement = font_manager.getGlyphFromChar(text_prim.getFontId(), c).advance
						if x_displacement + next_displacement > self.cursor_local_x + rect.x:
							# If the cursor is closer to the next intersection, wait
							if 2 * x_displacement + next_displacement >= 2 * (self.cursor_local_x + rect.x):
								break
						x_displacement += next_displacement
						p += 1
					self.cursor_position = p
					self.cursor_local_x = None
				else:
					for p in range(self.cursor_position):
						char = text[p]
						x_displacement += font_manager.getGlyphFromChar(text_prim.getFontId(), char).advance

			cursor_rect = Rect(x_displacement, y_position, 2, int(text_size * 1.2))
			self._addNewPrimitive(Rectangle, renderer, cursor_rect, text_color)

	def onHover(self, local_x, local_y):
		self.is_hovered = True
		return False

	def onClick(self, local_x, local_y):
		self.state = ACTIVE
		self.cursor_local_x = local_x
		return True

	def onOut(self):
		self.is_hovered = False
		self.mouse_position = None
		return False

	def onWindowClick(self):
		if not self.is_hovered:
			self.state = INACTIVE
			return True
		return False

	def onTextInput(self, text):
		character_limit = int(self.attributes["character-limit"])
		if self.state == ACTIVE:
			# Special character
			label = self.attributes["label"]
			p = self.cursor_position
			if text == "BACKSPACE":
				self.attributes["label"] = label[:p-1] + label[p:]
				self.cursor_position -= 1
			elif len(self.attributes["label"]) < character_limit:
				# Add text to the label
				self.cursor_position += 1
				self.attributes["label"] = label[:p] + text + label[p:]
			return True
		return False
