from ..blueprint.picture import Picture
from .element import Element
from .color import Color, lighthen
from .const import *

class Image(Element):
	def __init__(self, name):
		super(Image, self).__init__(name)
		# Specific to the Button element
		self.attributes = {
			"source": "",
			"adjust": "fill",
		}

	def build(self, renderer, rect):
		# Bluid blueprint
		I = Picture(self.attributes["source"], self.attributes["adjust"])
		I.build(renderer, rect, None)
		self.blueprint.append(I)
