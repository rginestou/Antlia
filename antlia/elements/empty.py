from .element import Element
from .const import *

class Empty(Element):
	def __init__(self, name):
		super(Empty, self).__init__(name)
		# Specific to the Button element
		self.attributes = {}

	def build(self, renderer, rect):
		pass
