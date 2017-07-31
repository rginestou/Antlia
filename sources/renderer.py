from .rect import Rect
import os
import sys
import ctypes
import numpy
from numpy import array

os.environ["PYSDL2_DLL_PATH"] = "lib/"
try:
	import sdl2
	import sdl2.sdlttf as sdl2ttf
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

class Renderer:
	"""
	The Renderer initializes an SLD2 context
	and gives the ability to draw elements on it.

	Renderer()
	Renderer.refresh()
	Renderer.quit()
	"""
	def __init__(self, onEvent, params):
		self.onEvent = onEvent
		self.is_window_created = False
		self.need_update = False
		self.params = params

		# Params
		self.window_width = int(self.params["resolution"][0])
		self.window_height = int(self.params["resolution"][1])

	def createWindow(self):
		# Create the window context
		if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
			print(sdl2.SDL_GetError())
			return -1
		sdl2ttf.TTF_Init()

		self.window = sdl2.SDL_CreateWindow(self.params["title"].encode(),
					   sdl2.SDL_WINDOWPOS_UNDEFINED,
					   sdl2.SDL_WINDOWPOS_UNDEFINED,
					   self.window_width,
					   self.window_height,
					   sdl2.SDL_WINDOW_OPENGL)
		if not self.window:
			print(sdl2.SDL_GetError())
			return -1

		# Renderer
		self.renderer = sdl2.SDL_CreateRenderer(self.window, -1,
            sdl2.SDL_RENDERER_ACCELERATED|sdl2.SDL_RENDERER_PRESENTVSYNC)

		# look for events
		self._loopForEvents()

	def update(self, layout_elements, layout_rects):
		self.layout_elements = layout_elements
		self.layout_rects = layout_rects
		self.need_update = True

	def quit(self):
		sdl2.SDL_DestroyRenderer(self.renderer)
		sdl2.SDL_HideWindow(self.window)
		sdl2.SDL_DestroyWindow(self.window)
		sdl2.SDL_Quit()

	def _refresh(self):
		"""
		Draws the GUI when it needs to be updated
		"""
		# Clear with white
		sdl2.SDL_SetRenderDrawColor(self.renderer, 255, 255, 255, 255);
		sdl2.SDL_RenderClear(self.renderer)

		# For each element of the layout, call its draw method
		for i, el in enumerate(self.layout_elements):
			el.draw(self.renderer, self.layout_rects[i])

		# Render to the screen
		sdl2.SDL_RenderPresent(self.renderer)

	def _loopForEvents(self):
		event = sdl2.SDL_Event()
		while True:
			# Look at the event queue
			while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
				self.onEvent(event)

			# Look for layout changes
			if self.need_update:
				self._refresh()
				self.need_update = False
			sdl2.SDL_Delay(5)
