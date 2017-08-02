from .translate import toArrayOfSizes, toInt
from ..blueprint.rectangle import Rectangle
from ..blueprint.text import Text
from ..blueprint.circle import Circle
from .element import Element
from ..rect import Rect
from .color import Color

class Progress(Element):
	def __init__(self, name):
		super(Progress, self).__init__(name)
		# Specific to the Button element
		self.attributes = {
			"selectable": False,
			"thickness": "12px",
			"completed": 80,
			"empty-color": "clouds",
			"full-color": "green-sea"
		}

	def build(self, renderer, rect):
		colors = {
			"empty-color": Color[self.attributes["empty-color"]],
			"full-color": Color[self.attributes["full-color"]]
		}

		height = rect.h

		t, typ_ = toArrayOfSizes(self.attributes["thickness"])
		if typ_ == "px":
			thickness = t[0]
		else:
			thickness = int(t[0] * height)

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		R.build(renderer,
				Rect(rect.x + int(thickness / 2),
					rect.y + int(height / 2 - thickness / 2),
					rect.w - thickness,
					thickness),
				colors["empty-color"])
		self.blueprint.append(R)

		completion = toInt(self.attributes["completed"])
		S = Rectangle(0.0, 0.0, 1.0, 1.0)
		S.build(renderer,
				Rect(rect.x + int(thickness / 2),
					rect.y + int(height / 2 - thickness / 2),
					(rect.w - thickness) * completion / 100.0,
					thickness),
				colors["full-color"])
		self.blueprint.append(S)
