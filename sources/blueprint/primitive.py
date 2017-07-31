import os

os.environ["PYSDL2_DLL_PATH"] = "lib/"
try:
	import sdl2
	import sdl2.ext as sdl2ext
	import sdl2.sdlttf as sdl2ttf
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

class Primitive:
	"""
	Defines a basic building bloc of a GUI element.
	It has some positionning attributes, and a Draw method.
	x, y, w, h are assumed to be within [0, 1]
	"""
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def draw(self, renderer, rect):
		pass
