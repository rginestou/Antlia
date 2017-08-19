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
