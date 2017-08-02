from .primitive import *
from ..rect import Rect
from .unicode import NAME_TO_UNICODE
import re


class Text(Primitive):
	def __init__(self, x, y, text, font, size, align="center"):
		super(Text, self).__init__(x, y, 1.0, 1.0)

		self.text = text
		self.size = int(size)
		self.font = sdl2ttf.TTF_OpenFont(font, self.size)
		self.align = align

		# TODO
		self.font_icon = sdl2ttf.TTF_OpenFont(b"resources/material-icons.ttf", self.size)
		self.font_text = sdl2ttf.TTF_OpenFont(b"resources/lato-regular.ttf", self.size)

	def build(self, renderer, rect, color):
		# Prepare text

		# Test if icon
		icon = re.compile(r'#(.+)#')

		s = icon.search(self.text)
		if s is not None:
			# Icon found !
			icon_name = s.group(1)
			self.text = NAME_TO_UNICODE[icon_name]

			font = self.font_icon
		else:
			font = self.font_text

		font = sdl2ttf.TTF_OpenFont(b"resources/material-icons.ttf", self.size)
		textSurface = sdl2ttf.TTF_RenderUTF8_Blended(font, self.text.encode(), sdl2.SDL_Color(*color), sdl2.SDL_Color(52,73,94,255))
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
		sdl2.SDL_FreeSurface(textSurface)

	def draw(self, renderer):
		sdl2.SDL_RenderCopy(renderer, self.textTexture, None, self.abs_rect)
