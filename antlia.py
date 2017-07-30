from sources.parser import Parser
from sources.renderer import Renderer
from sources.builder import Builder
from sources.message import log, ERROR, WARNING, OK
from sources.user import User
from sources.elements.const import *
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

	def bind(self, element_name, handler):
		"""
		Binds an element of the GUI with an handler.
		"""
		try:
			self.handlers[element_name] = handler
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
		try:
			self.layout_elements[element_index].setAttribute(parameter, value)
		except:
			log(WARNING, parameter + " is not a parameter of " + element_name)
			return

		# Need to refresh the GUI
		self._update()

	def getUserInfo(self):
		return self.user

	def quit(self):
		"""
		Before the program stops, clean everything properly
		"""
		self.is_running = False
		self.renderer.quit()

	def _update(self):
		"""
		Fill the renderer with the layout elements to draw,
		and the corresponding rects
		"""
		self.renderer.update(self.layout_elements, self.layout_rects)

	def _onEvent(self, event):
		# QUIT event
		if event.type == sdl2.SDL_QUIT:
			self.user.want_to_stop = True
		# MOUSE MOTION events
		if event.type == sdl2.SDL_MOUSEMOTION:
			X = event.motion.x
			Y = event.motion.y

			# Get the hovered elements
			current_indices = self._findHoveredElements(X, Y)

			# Look for the elements that are now hovered,
			# and those who are no more
			new_indices = [i for i in current_indices if i not in self.hovered_indices]
			old_indices = [i for i in self.hovered_indices if i not in current_indices]

			for i in new_indices:
				self.layout_elements[i].onHover()
			for i in old_indices:
				self.layout_elements[i].onOut()
			if len(new_indices) + len(old_indices) > 0:
				# Update if need be
				self._update()

			self.hovered_indices = current_indices
		if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
			for i in self.hovered_indices:
				self.layout_elements[i].onClick()
			if len(self.hovered_indices) > 0:
				self._update()
		if event.type == sdl2.SDL_MOUSEBUTTONUP:
			for i in self.hovered_indices:
				self.layout_elements[i].onRelease()
			if len(self.hovered_indices) > 0:
				self._update()
		# KEYBOARD events
		elif event.type == sdl2.SDL_KEYDOWN:
			# A key has been pressed
			if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
				self.user.want_to_stop = True
			elif event.key.keysym.sym == sdl2.SDLK_SPACE:
				pass

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
