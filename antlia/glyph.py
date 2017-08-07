import ctypes

import os
import pkg_resources

RESOURCES_PATH = pkg_resources.resource_filename('antlia', 'resources/')
LIB_PATH = pkg_resources.resource_filename('antlia', 'lib/')

os.environ["PYSDL2_DLL_PATH"] = LIB_PATH
try:
	import sdl2
	import sdl2.sdlttf as sdl2ttf
	import sdl2.sdlimage as sdl2img
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

class Glyph:
	minx = None
	maxx = None
	miny = None
	maxy = None
	advance = None

class GlyphTable:
	"""
	Contains all the glyphs for a given font
	"""
	def __init__(self, font):
		self.font = font
		self.glyphs = []

		self._buildGlyph()

	def get(self, character):
		c = ord(character)
		if c < 32 or c > 126:
			return None
		else:
			return self.glyphs[c - 32]

	def _buildGlyph(self):
		# Pointers
		p_minx = ctypes.pointer(ctypes.c_long(0))
		p_maxx = ctypes.pointer(ctypes.c_long(0))
		p_miny = ctypes.pointer(ctypes.c_long(0))
		p_maxy = ctypes.pointer(ctypes.c_long(0))
		p_advance = ctypes.pointer(ctypes.c_long(0))

		for c in range(32, 127):
			sdl2ttf.TTF_GlyphMetrics(self.font, c, p_minx, p_maxx, p_miny, p_maxy, p_advance)

			G = Glyph()
			G.minx = p_minx.contents.value
			G.maxx = p_maxx.contents.value
			G.miny = p_miny.contents.value
			G.maxy = p_maxy.contents.value
			G.advance = p_advance.contents.value

			self.glyphs.append(G)
