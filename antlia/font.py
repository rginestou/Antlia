from .glyph import GlyphTable

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

class FontManager:
	"""
	Stores all fonts here.
	This dictionnary contains the TTF font along with the glyph table.

	Supported fonts:
	- lato light
	- roboto light
	"""
	def __init__(self):
		self.supported_fonts_path = {
			"icons": RESOURCES_PATH + "material-icons.ttf",
			"roboto-light": RESOURCES_PATH + "roboto-light.ttf",
			"lato-light": RESOURCES_PATH + "lato-light.ttf"
		}
		# (TTF, Glyph, font_id)
		self.font_table = []
		#  "roboto***15": 15
		self.font_hashes = {}

		self.font_id = 0

	def addFont(self, font_path, size):
		font_hash = font_path + "***" + str(size)
		if font_hash in self.font_hashes:
			# If the font already exist, return its font_id
			return self.font_hashes[font_hash]

		if font_path in self.supported_fonts_path:
			# Supported path
			font_path = self.supported_fonts_path[font_path]

		self.font_hashes[font_hash] = self.font_id

		font = sdl2ttf.TTF_OpenFont(font_path.encode(), size)
		# Check for errors
		errors = sdl2ttf.TTF_GetError()
		if errors:
			print("Add font", errors)

		self.font_table.append((font, GlyphTable(font)))
		self.font_id += 1
		return self.font_id - 1

	def getGlyphFromChar(self, font_id, character):
		return self.font_table[font_id][1].get(character)

	def getFont(self, font_id):
		return self.font_table[font_id][0]

	def destroy(self):
		pass
		# TODO
		# sdl2ttf.TTF_CloseFont(self.font_icon)
		# sdl2ttf.TTF_CloseFont(self.font_text)
