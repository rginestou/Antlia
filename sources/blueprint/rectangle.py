from .primitive import *
from ..rect import Rect

class Rectangle(Primitive):
	def __init__(self, x, y, w, h):
		super(Rectangle, self).__init__(x, y, w, h)

	def build(self, renderer, rect, color):
		self.color = color
		# Compute the square in absolute coordinates
		rectangle_rect = Rect(self.x, self.y, self.w, self.h)
		self.abs_rect = sdl2.SDL_Rect(*rectangle_rect.fitRect(rect).getTuple())

	def draw(self, renderer):
		# Draw with SDL2
		sdl2.SDL_SetRenderDrawColor(renderer, *self.color)
		sdl2.SDL_RenderFillRect(renderer, self.abs_rect)
