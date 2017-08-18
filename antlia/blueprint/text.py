from .primitive import *
from ..rect import Rect
from .unicode import NAME_TO_UNICODE
import re
import time as ti

class Text(Primitive):
	def __init__(self, text, font_path, size, align="center"):
		super(Text, self).__init__()

		self.text = text
		self.size = int(size)
		self.align = align

		# Test if icon
		icon = re.compile(r'#(.+)#')

		s = icon.search(self.text)
		if s is not None:
			# Icon found !
			icon_name = s.group(1)
			self.text = NAME_TO_UNICODE[icon_name]

			# Add font to the font manager
			self.font_id = font_manager.addFont("icons", self.size)
		else:
			self.font_id = font_manager.addFont(font_path, self.size)
		self.font = font_manager.getFont(self.font_id)

	def build(self, renderer, rect, color):
		if self.text != "":
			textSurface = sdl2ttf.TTF_RenderUTF8_Blended(self.font, self.text.encode(),
														sdl2.SDL_Color(*color),
														sdl2.SDL_Color(52,73,94,255))
			errors = sdl2ttf.TTF_GetError()
			if errors:
				print("Text", errors)
			w = textSurface.contents.w
			h = textSurface.contents.h

			# Compute the square in absolute coordinates
			X = rect.x
			Y = int(rect.y + rect.h /2 - h/2)
			if self.align == "center":
				X = int(X + rect.w /2 - w/2)
			if self.align == "right":
				X = int(X + rect.w - w)
			self.abs_rect = sdl2.SDL_Rect(X, Y, w, h)

			self.textTexture = sdl2.SDL_CreateTextureFromSurface(renderer, textSurface)
			sdl2.SDL_FreeSurface(textSurface)

	def draw(self, renderer):
		if self.text != "":
			sdl2.SDL_RenderCopy(renderer, self.textTexture, None, self.abs_rect)

	def getFontId(self):
		return self.font_id

	def destroy(self):
		if self.text != "":
			sdl2.SDL_DestroyTexture(self.textTexture)
