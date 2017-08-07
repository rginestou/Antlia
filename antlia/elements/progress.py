from .translate import toArrayOfSizes, toFloat
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
			"thickness": "10px",
			"completed": 50,
			"empty-color": "clouds",
			"full-color": "green-sea",
			"padding": "0px"
		}

	def build(self, renderer, rect):
		self._clearBlueprint()

		colors = {
			"empty-color": Color[self.attributes["empty-color"]],
			"full-color": Color[self.attributes["full-color"]]
		}

		# Apply padding
		rect = rect.getPaddingRect(self.attributes["padding"])

		height = rect.h
		width = rect.w

		t, typ_, err = toArrayOfSizes(self.attributes["thickness"])
		if typ_ == "px":
			thickness = t[0]
		else:
			thickness = int(t[0] * height)

		Cleft = Circle(0.5, 0.5, 0.5)
		Cleft.build(renderer, Rect(rect.x,
								rect.y + int(height / 2 - thickness / 2),
								thickness, thickness),
				colors["empty-color"])
		self.blueprint.append(Cleft)
		Cright = Circle(0.5, 0.5, 0.5)
		Cright.build(renderer, Rect(rect.x + width - thickness,
								rect.y + int(height / 2 - thickness / 2),
								thickness, thickness),
				colors["empty-color"])
		self.blueprint.append(Cright)

		# Bluid blueprint
		R = Rectangle(0.0, 0.0, 1.0, 1.0)
		R.build(renderer,
				Rect(rect.x + int(thickness / 2),
					rect.y + int(height / 2 - thickness / 2),
					rect.w - thickness,
					thickness+1), # For the circle to be aligned
				colors["empty-color"])
		self.blueprint.append(R)

		completion = toFloat(self.attributes["completed"])
		if completion > 0.0:
			comp_width = (rect.w - thickness) * completion / 100.0

			Ccompleft = Circle(0.5, 0.5, 0.5)
			Ccompleft.build(renderer, Rect(rect.x,
									rect.y + int(height / 2 - thickness / 2),
									thickness, thickness),
					colors["full-color"])
			self.blueprint.append(Ccompleft)
			Ccompright = Circle(0.5, 0.5, 0.5)
			Ccompright.build(renderer, Rect(rect.x + comp_width,
									rect.y + int(height / 2 - thickness / 2),
									thickness, thickness),
					colors["full-color"])
			self.blueprint.append(Ccompright)

			S = Rectangle(0.0, 0.0, 1.0, 1.0)
			S.build(renderer,
					Rect(rect.x + int(thickness / 2),
						rect.y + int(height / 2 - thickness / 2),
						comp_width,
						thickness+1),
					colors["full-color"])
			self.blueprint.append(S)
