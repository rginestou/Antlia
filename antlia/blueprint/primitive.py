import os, sys
import pkg_resources

RESOURCES_PATH = pkg_resources.resource_filename('antlia', 'resources/')
LIB_PATH = pkg_resources.resource_filename('antlia', 'lib/')

os.environ["PYSDL2_DLL_PATH"] = LIB_PATH
try:
	import sdl2
	import sdl2.ext as sdl2ext
	import sdl2.sdlttf as sdl2ttf
	import sdl2.sdlimage as sdl2img
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

	def build(self, renderer, rect, color):
		pass

	def draw(self, renderer):
		pass
