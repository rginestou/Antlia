from ..blueprint.picture import Picture
from .element import Element
from .color import Color, lighthen
from .const import *

class Image(Element):
	def __init__(self, name):
		super(Image, self).__init__(name)
		self.type = "image"

		# Specific to the Button element
		self.attributes = {
			"source": "",
			"adjust": "fill",
			"padding": "0px"
		}

	def build(self, renderer, rect):
		# Apply padding
		img_rect = rect.getPaddingRect(self.attributes["padding"])

		if self.attributes["source"] == "":
			return

		### Bluid blueprint ###
		self._clearBlueprint()

		self._addNewPrimitive(Picture, renderer, img_rect, None, args=(
			self.attributes["source"],
			self.attributes["adjust"]
		))
