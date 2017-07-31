from .primitive import *
from ..rect import Rect

class Text(Primitive):
	def __init__(self, x, y, text, font, color, align="center"):
		super(Text, self).__init__(x, y, 1.0, 1.0)

		self.text = text
		self.font = sdl2ttf.TTF_OpenFont(font, 21)
		self.align = align

	def draw(self, renderer, rect, color):
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
		abs_rect = sdl2.SDL_Rect(X, Y, w, h)

		# Draw with SDL2
		textTexture = sdl2.SDL_CreateTextureFromSurface(renderer, textSurface)
		sdl2.SDL_RenderCopy(renderer, textTexture, None, abs_rect)
