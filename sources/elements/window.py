from .element import Element
from ..rect import Rect

class Window(Element):
	def __init__(self):
		super(Window, self).__init__()
		# Specific to the Button element
		self.attributes = {
			"title": "Untitled window",
			"resolution": {"width": 800, "height": 400},
			"fullscreen": False
		}

		# By default, the window has only one child
		self.child_rects = [Rect(0.0, 0.0, 1.0, 1.0)]