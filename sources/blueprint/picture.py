from .primitive import *
from ..rect import Rect

class Picture(Primitive):
	def __init__(self, src, adjust):
		self.src = src
		self.adjust = adjust
		super(Picture, self).__init__(0.0, 0.0, 1.0, 1.0)

	def build(self, renderer, rect, color):
		# Prepare image
		imgSurface = sdl2img.IMG_Load(self.src.encode());
		errors = sdl2img.IMG_GetError()
		if errors:
			print(errors)
			return

		w = imgSurface.contents.w
		h = imgSurface.contents.h

		# Compute the square in absolute coordinates
		text_rect = Rect(self.x, self.y, self.w, self.h)
		_rect = Rect(*text_rect.fitRect(rect).getTuple())
		X = _rect.x
		Y = int(_rect.y - h/2)
		if self.adjust == "center":
			X = int(X - w/2)
		if self.adjust == "right":
			X = int(X - w)
		self.abs_rect = sdl2.SDL_Rect(X, Y, w, h)

		self.imgTexture = sdl2.SDL_CreateTextureFromSurface(renderer, imgSurface)

	def draw(self, renderer):
		sdl2.SDL_RenderCopy(renderer, self.imgTexture, None, self.abs_rect)
