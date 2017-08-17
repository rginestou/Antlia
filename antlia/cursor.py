import pkg_resources
from .elements.const import *
import os

LIB_PATH = pkg_resources.resource_filename('antlia', 'lib/')

os.environ["PYSDL2_DLL_PATH"] = LIB_PATH
try:
	import sdl2
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

def changeCursor(t):
	if t == WAIT:
		cursor = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_WAIT)
	elif t == TEXT:
		cursor = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_IBEAM)
	else:
		cursor = sdl2.SDL_CreateSystemCursor(sdl2.SDL_SYSTEM_CURSOR_ARROW)
	sdl2.SDL_SetCursor(cursor)
