from .translate import toArrayOfSizes, toFloat
from ..message import catch, ERROR, WARNING, OK
from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from ..blueprint.circle import Circle
from .element import Element
from .slider import Slider
from ..rect import Rect
from .color import Color

class Progress(Element):
	def __init__(self, name):
		super(Progress, self).__init__(name)
		self.type = "progress"

		# Specific to the Button element
		self.attributes = {
			"selectable": False,
			"thickness": "10px",
			"completed": 50,
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

		# Get completion
		t, typ_ = catch(
			toArrayOfSizes, (self.attributes["thickness"],),
			ERROR, self.name + " .thickness")
		if typ_[0] == "px":
			thickness = t[0]
		else:
			thickness = int(t[0] * length)
		completion = toFloat(self.attributes["completed"])
		slider_size = int((rect.w - thickness) * completion / 100.0)

		### Bluid blueprint ###
		self._addNewElement(Slider, renderer, rect, {
			"selectable": self.attributes["selectable"],
			"thickness": str(thickness) + "px",
			"slider-size": str(slider_size) + "px",
			"empty-color": self.attributes["empty-color"],
			"full-color": self.attributes["full-color"],
		})

		# height = rect.h
		# width = rect.w
		#
		# t, typ_ = catch(
		# 	toArrayOfSizes, (self.attributes["thickness"],),
		# 	ERROR, self.name + " .thickness:")
		# if typ_[0] == "px":
		# 	thickness = t[0]
		# else:
		# 	thickness = int(t[0] * height)
		# comp_width = int((rect.w - thickness) * completion / 100.0)
		#
		# # Compute rects
		# left_circle_rect = Rect(rect.x, int(rect.y + int(height / 2 - thickness / 2)), thickness, thickness)
		# right_circle_rect = Rect(rect.x + width - thickness, left_circle_rect.y, thickness, thickness)
		# right_comp_circle_rect = Rect(rect.x + comp_width, left_circle_rect.y, thickness, thickness)
		# back_rect = Rect(
		# 	rect.x + int(thickness / 2),
		# 	left_circle_rect.y,
		# 	rect.w - thickness,
		# 	thickness+1) # For the circle to be aligned
		# front_rect = Rect(
		# 	back_rect.x,
		# 	back_rect.y,
		# 	comp_width,
		# 	back_rect.h)
		#
		#
		# ### Bluid blueprint ###
		# self._clearBlueprint()
		#
		# # Background shape
		# self._addNewPrimitive(Circle, renderer, left_circle_rect, colors["empty"])
		# self._addNewPrimitive(Circle, renderer, right_circle_rect, colors["empty"])
		# self._addNewPrimitive(Rectangle, renderer, back_rect, colors["empty"])
		#
		# if completion > 0.0:
		# 	# Foreground shape
		# 	self._addNewPrimitive(Circle, renderer, left_circle_rect, colors["full"])
		# 	self._addNewPrimitive(Circle, renderer, right_comp_circle_rect, colors["full"])
		# 	self._addNewPrimitive(Rectangle, renderer, front_rect, colors["full"])
