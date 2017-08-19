from .translate import toArrayOfSizes, toFloat
from ..message import catch, ERROR, WARNING, OK
from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from ..blueprint.circle import Circle
from .element import Element
from ..rect import Rect
from .color import Color

class Slider(Element):
	def __init__(self, name):
		super(Slider, self).__init__(name)
		self.type = "slider"

		# Specific to the Button element
		self.attributes = {
			"selectable": True,
			"thickness": "10px",
			"align": "horizontal",
			"slider-size": "50%",
			"slider-position": "0%",
			"empty-color": "clouds",
			"full-color": "green-sea",
			"padding": "0px"
		}

	def build(self, renderer, rect):
		# Apply padding
		rect = rect.getPaddingRect(self.attributes["padding"])

		# Fetch colors
		colors = {
			"empty": Color[self.attributes["empty-color"]],
			"full": Color[self.attributes["full-color"]]
		}

		height = rect.h
		width = rect.w
		align = self.attributes["align"]
		if align == "vertical":
			length = height
		else:
			length = width

		s, typ_ = catch(
			toArrayOfSizes, (self.attributes["slider-position"],),
			ERROR, self.name + " .slider-position")
		if typ_[0] == "px":
			slider_pos = s[0]
		else:
			slider_pos = int(s[0] * length)

		s, typ_ = catch(
			toArrayOfSizes, (self.attributes["slider-size"],),
			ERROR, self.name + " .slider-size")
		if typ_[0] == "px":
			slider_length = s[0]
		else:
			slider_length = int(s[0] * length)

		t, typ_ = catch(
			toArrayOfSizes, (self.attributes["thickness"],),
			ERROR, self.name + " .thickness")
		if typ_[0] == "px":
			thickness = t[0]
		else:
			thickness = int(t[0] * length)

		# Compute rects
		left_circle_rect = Rect(rect.x, int(rect.y + int(height / 2 - thickness / 2)), thickness, thickness)
		right_circle_rect = Rect(rect.x + width - thickness, left_circle_rect.y, thickness, thickness)
		left_comp_circle_rect = Rect(rect.x + slider_pos, left_circle_rect.y, thickness, thickness)
		right_comp_circle_rect = Rect(rect.x + slider_pos + slider_length, left_circle_rect.y, thickness, thickness)
		back_rect = Rect(
			rect.x + int(thickness / 2),
			left_circle_rect.y,
			rect.w - thickness,
			thickness + (1 - thickness % 2)) # For the circle to be aligned
		front_rect = Rect(
			back_rect.x + slider_pos,
			back_rect.y,
			slider_length,
			back_rect.h)
		if align == "vertical":
			left_circle_rect.x, left_circle_rect.y = left_circle_rect.y, left_circle_rect.x
			right_circle_rect.x, right_circle_rect.y = right_circle_rect.y, right_circle_rect.x
			right_comp_circle_rect.x, right_comp_circle_rect.y = right_comp_circle_rect.y, right_comp_circle_rect.x
			back_rect.x, back_rect.y = back_rect.y, back_rect.x
			back_rect.w, back_rect.h = back_rect.h, back_rect.w
			front_rect.x, front_rect.y = front_rect.y, front_rect.x
			front_rect.w, front_rect.h = front_rect.h, front_rect.w

		### Bluid blueprint ###
		self._clearBlueprint()

		# Background shape
		self._addNewPrimitive(Circle, renderer, left_circle_rect, colors["empty"])
		self._addNewPrimitive(Circle, renderer, right_circle_rect, colors["empty"])
		self._addNewPrimitive(Rectangle, renderer, back_rect, colors["empty"])

		if slider_length > 0:
			# Foreground shape
			self._addNewPrimitive(Circle, renderer, left_comp_circle_rect, colors["full"])
			self._addNewPrimitive(Circle, renderer, right_comp_circle_rect, colors["full"])
			self._addNewPrimitive(Rectangle, renderer, front_rect, colors["full"])
