from .primitive import *
from ..rect import Rect

class Text(Primitive):
	def __init__(self, x, y, text, font, color, align="center"):
		# TODO
		w = 10 * len(text)
		h = 15
		super(Rectangle, self).__init__(x, y, w, h, color)

		self.text = text
		self.font = font
		self.align = align

	def draw(self, rect, color):
		# Compute the square in absolute coordinates
		abs_rect = sdl2.SDL_Rect(*rect.fitRect().getTuple())

		# Draw with SDL2
		sdl2.SDL_SetRenderDrawColor(self.renderer, *self.color)
		sdl2.SDL_RenderFillRect(self.renderer, abs_rect)
