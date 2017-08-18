import os, sys
import pkg_resources
from ..font import FontManager

RESOURCES_PATH = pkg_resources.resource_filename('antlia', 'resources/')
LIB_PATH = pkg_resources.resource_filename('antlia', 'lib/')

os.environ["PYSDL2_DLL_PATH"] = LIB_PATH
try:
	import sdl2
	import sdl2.ext as sdl2ext
	import sdl2.sdlttf as sdl2ttf
	import sdl2.sdlimage as sdl2img
	import sdl2.sdlgfx as sdl2gfx
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

# Unique instance of FontManager
font_manager = FontManager()

class Primitive:
	"""
	Defines a basic building bloc of a GUI element.
	Some arguments can be passed as a dictionnary
	"""
	def __init__(self):
		pass

	def build(self, renderer, rect, color):
		pass

	def destroy(self):
		pass

	def draw(self, renderer):
		pass
