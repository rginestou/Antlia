from .primitive import *
from ..rect import Rect

class Rectangle(Primitive):
	def __init__(self):
		super(Rectangle, self).__init__()

	def build(self, renderer, rect, color):
		self.color = color

		# Compute the square in absolute coordinates
		self.abs_rect = sdl2.SDL_Rect(*rect.getTuple())

	def draw(self, renderer):
		# Draw with SDL2
		if self.color is not None:
			sdl2.SDL_SetRenderDrawColor(renderer, *self.color)
			sdl2.SDL_RenderFillRect(renderer, self.abs_rect)
