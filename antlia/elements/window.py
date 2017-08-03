from .element import Element
from ..rect import Rect

class Window(Element):
	def __init__(self, name):
		super(Window, self).__init__(name)
		# Specific to the Button element
		self.attributes = {
			"title": "Untitled window",
			"resolution": "800px 400px",
			"fullscreen": False,
			"show-borders": True
		}

		# By default, the window has only one child
		self.child_rects = [Rect(0.0, 0.0, 1.0, 1.0)]
