from .primitive import *
from ..rect import Rect

class Text(Primitive):
	def __init__(self, x, y, text, font, align="center"):
		super(Text, self).__init__(x, y, 1.0, 1.0)

		self.text = text
		self.font = sdl2ttf.TTF_OpenFont(font, 21)
		self.align = align

	def build(self, renderer, rect, color):
		# Prepare text
		font = sdl2ttf.TTF_OpenFont(b"resources/roboto-light.ttf", 41)
		textSurface = sdl2ttf.TTF_RenderText_Blended(font, self.text.encode(), sdl2.SDL_Color(*color))
		w = textSurface.contents.w
		h = textSurface.contents.h

		# Compute the square in absolute coordinates
		text_rect = Rect(self.x, self.y, self.w, self.h)
		_rect = Rect(*text_rect.fitRect(rect).getTuple())
		X = _rect.x
		Y = int(_rect.y - h/2)
		if self.align == "center":
			X = int(X - w/2)
		if self.align == "right":
			X = int(X - w)
		self.abs_rect = sdl2.SDL_Rect(X, Y, w, h)

		self.textTexture = sdl2.SDL_CreateTextureFromSurface(renderer, textSurface)

	def draw(self, renderer):
		sdl2.SDL_RenderCopy(renderer, self.textTexture, None, self.abs_rect)
