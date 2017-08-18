from .primitive import *
from ..rect import Rect

class Circle(Primitive):
	def __init__(self):
		super(Circle, self).__init__()

	def build(self, renderer, rect, color):
		self.color = color

		self.x = rect.x + rect.w // 2
		self.y = rect.y + rect.h // 2
		self.radius = rect.w // 2

	def draw(self, renderer):
		# Draw with SDL2
		sdl2gfx.filledCircleRGBA(renderer, self.x, self.y, self.radius, *self.color)
		sdl2gfx.aacircleRGBA(renderer, self.x, self.y, self.radius, *self.color)
