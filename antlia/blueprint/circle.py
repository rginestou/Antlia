from .primitive import *
from ..rect import Rect

class Circle(Primitive):
	def __init__(self, x, y, radius):
		w = h = 10
		super(Circle, self).__init__(x, y, w, h)

		self.radius = radius

	def build(self, renderer, rect, color):
		self.color = color
		diam = 2 * self.radius

		self.X = int(rect.x + rect.w * self.x)
		self.Y = int(rect.y + rect.h * self.y)
		self.Radius = int(rect.w * self.radius)

	def draw(self, renderer):
		# Draw with SDL2
		sdl2gfx.filledCircleRGBA(renderer, self.X, self.Y, self.Radius, *self.color)
		sdl2gfx.aacircleRGBA(renderer, self.X, self.Y, self.Radius, *self.color)
