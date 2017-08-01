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

		imW = imgSurface.contents.w
		imH = imgSurface.contents.h

		# Compute the square in absolute coordinates
		box_rect = Rect(self.x, self.y, self.w, self.h)
		self.abs_rect = sdl2.SDL_Rect(*box_rect.fitRect(rect).getTuple())
		W = self.abs_rect.w
		H = self.abs_rect.h

		if self.adjust == "fill": #TODO
			self.img_rect = sdl2.SDL_Rect(0, 0, imW, imH)
		elif self.adjust == "stretch":
			self.img_rect = sdl2.SDL_Rect(0, 0, imW, imH)
		elif self.adjust == "center":
			self.img_rect = sdl2.SDL_Rect(int(imW / 2 - W / 2), int(imH / 2 - W / 2), W, H)
		else:
			self.img_rect = sdl2.SDL_Rect(int(imW / 2 - W / 2), int(imH / 2 - W / 2), W, H)

		self.imgTexture = sdl2.SDL_CreateTextureFromSurface(renderer, imgSurface)
		sdl2.SDL_FreeSurface(imgSurface)

	def draw(self, renderer):
		sdl2.SDL_RenderCopy(renderer, self.imgTexture, self.img_rect, self.abs_rect)
