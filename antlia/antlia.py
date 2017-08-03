import os
import threading
import ctypes
import time as ti
import pkg_resources

LIB_PATH = pkg_resources.resource_filename('antlia', 'lib/')

os.environ["PYSDL2_DLL_PATH"] = LIB_PATH
try:
	import sdl2
	import sdl2.sdlttf as sdl2ttf
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

from .parser import Parser
from .renderer import Renderer
from .builder import Builder
from .message import log, ERROR, WARNING, OK
from .user import User
from .elements.const import *
from .dialog import getOpenFileName

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
		self.is_window_focused = True
		self.path = os.getcwd()

		# The Parser that will read all informations from both
		# the layout and style files
		self.parser = Parser(self.layout_file_name, self.style_file_name)
		self.handlers = self.parser.getHandlers()
		self.layout_elements = self.parser.getLayoutElements()
		self.layout_tree = self.parser.getLayoutTree()
		self.layout_table = self.parser.getLayoutTable()
		self.layout_rects = None

		# Fetch window parameters
		window_parameters = self.layout_elements[0].getAttributes()

		# The Renderer will take a reference to the layout to display it
		self.renderer = Renderer(self._onEvent, params=window_parameters)

		# The layout structure is passed to the builder to construct
		# the vertex buffer data displayed by OpenGL
		self.builder = Builder(params=window_parameters)

		# Keep track of hovered elements for optimisation sake
		self.hovered_indices = []

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

		# Give the info to the renderer
		self._update()

	def bind(self, element_name, event_type, handler, arg=None):
		"""
		Binds an element of the GUI with an handler.
		"""
		try:
			if element_name not in self.handlers:
				self.handlers[element_name] = {}
			self.handlers[element_name][event_type] = (handler, arg)
		except KeyError:
			log(WARNING, element_name + " does not exist in the layout")

	def change(self, element_name, parameter, value):
		"""
		Changes an element's parameter value
		"""
		# Fetch the element
		try:
			element_index = self.layout_table[element_name]
		except KeyError:
			log(WARNING, element_name + " does not exist in the layout")
			return

		# Change the parameter
		self.layout_elements[element_index].setAttribute(parameter, value)
		self.renderer.buildElements() #TODO
		# self.layout_elements[element_index].build()

		# Need to refresh the GUI
		self._update()
		self.renderer.buildElements()

	def getUserInfo(self):
		return self.user

	def stop(self):
		self.user.want_to_stop = True

	def quit(self):
		"""
		Before the program stops, clean everything properly
		"""
		self.is_running = False
		self.renderer.quit()

	def openFileDialog(self, title, default_extension, filter_string, initialPath):
		file_path_buff = getOpenFileName(title, default_extension, filter_string, initialPath)

		if file_path_buff is not None:
			file_path = file_path_buff.replace("\x00", "")
		else:
			file_path = None

		# Change current directory !
		os.chdir(self.path)

		return file_path

	def _update(self):
		"""
		Fill the renderer with the layout elements to draw,
		and the corresponding rects
		"""
		self.renderer.update(self.layout_elements, self.layout_rects)

	def _buildElements(self):
		self.renderer.buildElements()

	def _buildElement(self, element_index):
		self.renderer.buildElement(element_index)

	def _onEvent(self, event):
		el_indices_to_rebuild = []

		# QUIT event
		if event.type == sdl2.SDL_QUIT:
			self.user.want_to_stop = True
		# MOUSE MOTION events
		elif event.type == sdl2.SDL_MOUSEMOTION:
			X = event.motion.x
			Y = event.motion.y

			# Get the hovered elements
			current_indices = self._findHoveredElements(X, Y)

			# Look for the elements that are now hovered,
			# and those who are no more
			new_indices = [i for i in current_indices if i not in self.hovered_indices]
			old_indices = [i for i in self.hovered_indices if i not in current_indices]

			# Fire hover handlers
			for i in new_indices:
				el = self.layout_elements[i]
				self._callHandler(el.name, "hover")
				el.onHover()

				# Need to be rebuilt
				el_indices_to_rebuild.append(i)
			for i in old_indices:
				self.layout_elements[i].onOut()

				# Need to be rebuilt
				el_indices_to_rebuild.append(i)

			self.hovered_indices = current_indices
		elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
			for i in self.hovered_indices:
				el = self.layout_elements[i]
				self._callHandler(el.name, "click")
				el.onClick()

				# Need to be rebuilt
				el_indices_to_rebuild.append(i)
		elif event.type == sdl2.SDL_MOUSEBUTTONUP:
			for i in self.hovered_indices:
				el = self.layout_elements[i]
				self._callHandler(el.name, "release")
				el.onRelease()

				# Need to be rebuilt
				el_indices_to_rebuild.append(i)
		# KEYBOARD events
		elif event.type == sdl2.SDL_KEYDOWN:
			# A key has been pressed
			if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
				self.user.want_to_stop = True
			elif event.key.keysym.sym == sdl2.SDLK_SPACE:
				pass
		# WINDOW events
		if event.type == sdl2.SDL_WINDOWEVENT:
			if event.window.event == sdl2.SDL_WINDOWEVENT_FOCUS_GAINED:
				self.is_window_focused = True
			if event.window.event == sdl2.SDL_WINDOWEVENT_FOCUS_LOST:
				self.is_window_focused = False

		# Rebuild all the elements
		for i in list(set(el_indices_to_rebuild)):
			self._buildElement(i)
			self.renderer.setUpdateNeed(True)

	def _findHoveredElements(self, X, Y):
		"""
		Given the coordinates of the mouse, find which rects
		are hovered.
		"""
		hovered_indices = []
		for i, rect in enumerate(self.layout_rects):
			if rect.isOver(X, Y):
				hovered_indices.append(i)

		return hovered_indices

	def _callHandler(self, element_name, event_type):
		if element_name in self.handlers and event_type in self.handlers[element_name]:
			params = self.handlers[element_name][event_type][1]
			if params is not None:
				self.handlers[element_name][event_type][0](params)
			else:
				self.handlers[element_name][event_type][0]()
