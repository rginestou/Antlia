from .primitive import *
from ..rect import Rect

class Rectangle(Primitive):
	def __init__(self, x, y, w, h):
		super(Rectangle, self).__init__(x, y, w, h)

	def draw(self, renderer, rect, color):
		# Compute the square in absolute coordinates
		rectangle_rect = Rect(self.x, self.y, self.w, self.h)
		abs_rect = sdl2.SDL_Rect(*rectangle_rect.fitRect(rect).getTuple())

		# Draw with SDL2
		sdl2.SDL_SetRenderDrawColor(renderer, color.R, color.G, color.B, 255)
		sdl2.SDL_RenderFillRect(renderer, abs_rect)
