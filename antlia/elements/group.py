from .element import Element
from .const import *

class Group(Element):
	def __init__(self, name):
		super(Group, self).__init__(name)
		self.type = "group"

	def placeChildren(self, rect, n_child):
		self.child_rects = [rect] * n_child
