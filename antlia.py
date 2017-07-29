from sources.parser import Parser
from sources.renderer import Renderer
from sources.builder import Builder
from sources.message import log, ERROR, WARNING, OK
from sources.user import User
import threading
import os
import ctypes

os.environ["PYSDL2_DLL_PATH"] = "lib/"
try:
	import sdl2
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

class Antlia:
	"""
	The Antlia Class is the only object the user of the library
	has access to. Once instanciated, it is used to manage the
	links between the elements of the GUI and the backend.
	"""
	def __init__(self, layout, style=None):
		self.layout_file_name = layout
		self.style_file_name = style
		self.is_running = True
		self.user = User()

		# The Parser that will read all informations from both
		# the layout and style files
		self.parser = Parser(self.layout_file_name, self.style_file_name)
		self.handlers = self.parser.getHandlers()
		self.layout_elements = self.parser.getLayoutElements()
		self.layout_tree = self.parser.getLayoutTree()
		self.layout_rects = None

		# The Renderer will take a reference to the layout to display it
		self.renderer = Renderer(self._onEvent, params=self.layout_elements[0].getAttributes())

		# The layout structure is passed to the builder to construct
		# the vertex buffer data displayed by OpenGL
		self.builder = Builder()

	def start(self):
		"""
		The event loop needs to be launched from the thread where
		the window has been lauched.
		"""
		# For instantaneity sake, precompute the data
		self.layout_rects = self.builder.computeLayoutRects(self.layout_elements, self.layout_tree)

		thread = threading.Thread(target=self.renderer.createWindow, args=())
		thread.daemon = True
		thread.start()

		# Fill the renderer with the layout elements to draw
		self.renderer.update(self.layout_elements, self.layout_rects)

	def bind(self, element_name, handler):
		"""
		Binds an element of the GUI with an handler.
		"""
		if element_name in self.handlers:
			self.handlers[element_name] = handler
		else:
			log(WARNING, element_name + " does not exist in the layout")

	def change(self, element_name, parameter, value):
		"""
		Changes an element's parameter value
		"""
		pass

	def getUserInfo(self):
		return self.user

	def quit(self):
		"""
		Before the program stops, clean everything properly
		"""
		self.is_running = False
		self.renderer.quit()

	def _update(self):
		self.renderer.update(self.layout_rects)

	def _onEvent(self, event):
		if event.type == sdl2.SDL_QUIT:
			self.user.want_to_stop = True
		elif (event.type == sdl2.SDL_KEYDOWN and
			event.key.keysym.sym == sdl2.SDLK_ESCAPE):
			self.user.want_to_stop = True
