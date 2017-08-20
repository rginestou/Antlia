import time as ti

import os
import threading
import ctypes
import pkg_resources

LIB_PATH = pkg_resources.resource_filename('antlia', 'lib/')

os.environ["PYSDL2_DLL_PATH"] = LIB_PATH
try:
	import sdl2
	import sdl2.sdlttf as sdl2ttf
	import sdl2.sdlgfx as sdl2gfx
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

from .parser import Parser
from .mouse import Mouse
from .renderer import Renderer
from .builder import Builder
from .elements.translate import toBoolean
from .message import catch, ERROR, WARNING, OK
from .user import User
from .elements.const import *
from .cursor import changeCursor
from .dialog import getOpenFileName
from .elements.const import *

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

		# Mouse
		self.mouse = Mouse()

		# The Parser that will read all informations from both
		# the layout and style files
		self.parser = Parser(self.layout_file_name, self.style_file_name)
		self.layout_elements = self.parser.getLayoutElements()
		self.layout_tree = self.parser.getLayoutTree()
		self.layout_table = self.parser.getLayoutTable()
		self.layout_rects = None
		self.validation_ids = {}

		# Handlers
		self.handlers = self.parser.getHandlers()
		self.startHandler = None
		self.text_input_hovered = False

		# Fetch window parameters
		window_parameters = self.layout_elements[0].getAttributes()

		# The Renderer will take a reference to the layout to display it
		self.renderer = Renderer(params=window_parameters)
		self.renderer.setOnEvent(self._onEvent)

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

		# Give time to create the window
		ti.sleep(1)

	def bind(self, element_name, event_type, handler, arg=None):
		"""
		Binds an element of the GUI with an handler.
		"""
		try:
			# TODO check if event type valid
			if element_name not in self.handlers:
				self.handlers[element_name] = {}
			self.handlers[element_name][event_type] = (handler, arg)
		except KeyError:
			log(WARNING, element_name + " does not exist in the layout")

	def onStart(self, handler, args=None):
		self.renderer.setOnStart(handler, args)

	def change(self, element_name, attribute, value):
		"""
		Changes an element's parameter value
		"""
		# Change the parameter
		element_index = self.parser.changeElement(element_name, attribute, value)
		self.layout_elements = self.parser.getLayoutElements()
		self.layout_tree = self.parser.getLayoutTree()

		# TODO change oly the element's tree
		self._update()
		self._buildElement(element_index)

	def add(self, element_type, element_name, parent, attributes={}):
		element_index = self.parser.addElement(element_type, element_name, parent, attributes)

		# Fetch new layout from parser
		self.layout_elements = self.parser.getLayoutElements()
		self.layout_tree = self.parser.getLayoutTree()
		self.layout_table = self.parser.getLayoutTable()

		# Rebuild layout
		self.layout_rects = self.builder.computeLayoutRects(self.layout_elements, self.layout_tree)
		self._update()
		self._buildElement(element_index)

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

	def isRunning(self):
		return self.is_running

	def _update(self):
		"""
		Fill the renderer with the layout elements to draw,
		and the corresponding rects
		"""
		# Update validation ids
		self.validation_ids = self.parser.buildFormValidation()

		self.renderer.update(self.layout_elements, self.layout_rects)

	def _buildElement(self, element_index):
		"""
		The rendering routine takes place in another thread.
		Therefore, only the indices are passed, and the renderer will
		notice it must rebuild them.
		"""
		self.renderer.addElementIndexToBuild(element_index)

	def _onEvent(self, event):
		el_indices_to_rebuild = []
		text_input = None

		# QUIT event
		if event.type == sdl2.SDL_QUIT:
			self.user.want_to_stop = True
		# KEYBOARD events
		elif event.type == sdl2.SDL_KEYDOWN:
			# A key has been pressed
			if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
				self.user.want_to_stop = True
			elif event.key.keysym.sym == sdl2.SDLK_BACKSPACE:
				text_input = "BACKSPACE"
			# print(sdl2.SDL_GetKeyName(event.key.keysym.sym))
		elif event.type == sdl2.SDL_TEXTINPUT:
			# Fire a text event to all elements
			text_input = event.text.text.decode()
		# MOUSE MOTION events
		elif event.type == sdl2.SDL_MOUSEMOTION:
			# Local mouse coordonates
			X = event.motion.x
			Y = event.motion.y

			# Global mouse coordonates
			gX = ctypes.pointer(ctypes.c_long(0))
			gY = ctypes.pointer(ctypes.c_long(0))
			sdl2.SDL_GetGlobalMouseState(gX, gY)
			global_X = gX.contents.value
			global_Y = gY.contents.value

			# Get the hovered elements
			current_hovered = self._findHoveredElements(X, Y)

			# Hovering text input ?
			found_text_input = False
			for h in current_hovered:
				if self.layout_elements[h[0]].type == "text-input":
					self.text_input_hovered = True
					found_text_input = True
			if not found_text_input:
				self.text_input_hovered = False


			# Look for draggable elements
			if self.mouse.left_click:
				dx = 0; dy = 0
				need_moving = False
				for h in current_hovered:
					el = self.layout_elements[h[0]]


					if el.hasAttribute("drag-window") and \
							catch(toBoolean, (el.getAttribute("drag-window"),),
							ERROR, el.name + " .drag-window"):
						dx = global_X - self.mouse.global_X
						dy = global_Y - self.mouse.global_Y
						need_moving = True

				if need_moving:
					wx, wy = self.renderer.getWindowPosition()
					self.renderer.setWindowPosition(wx + dx, wy + dy)

			# Look for the elements that are now hovered,
			# and those who are no more
			new_hovered = [x for x in current_hovered if x[0] not in self.hovered_indices]
			old_indices = []

			for o,_,_ in self.hovered_indices:
				still = False
				for n in current_hovered:
					if n[0] == o:
						# Still hovered
						still = True
						break
				if not still:
					old_indices.append(o)

			# Fire hover handlers
			for h in new_hovered:
				new_index = h[0]
				el = self.layout_elements[new_index]
				self._callHandler(el.name, "hover")

				# Pass local coordinates too
				el.onHover(h[1], h[2])

				# Need to be rebuilt
				el_indices_to_rebuild.append(new_index)
			for h in old_indices:
				self.layout_elements[h].onOut()

				# Need to be rebuilt
				el_indices_to_rebuild.append(h)

			# Update hovered indices
			self.hovered_indices = []
			for h in current_hovered:
				self.hovered_indices.append(h)

			# Update mouse position
			self.mouse.X = X
			self.mouse.Y = Y

			self.mouse.global_X = global_X
			self.mouse.global_Y = global_Y
		elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
			self.mouse.left_click = True

			# Fire a windowClick event to everyone
			for i, el in enumerate(self.layout_elements):
				if el.onWindowClick():
					el_indices_to_rebuild.append(i)

			for h in self.hovered_indices:
				element_index = h[0]
				el = self.layout_elements[element_index]
				self._callHandler(el.name, "click")
				el.onClick(h[1], h[2])

				valid_form_index = self.validation_ids.get(element_index, None)
				if valid_form_index is not None:
					form_name = self.layout_elements[valid_form_index].name
					fields = self.parser.buildFormFields(valid_form_index)
					self._callHandler(form_name, "validation", extra_params=fields)

				# Need to be rebuilt
				el_indices_to_rebuild.append(i)
		elif event.type == sdl2.SDL_MOUSEBUTTONUP:
			self.mouse.left_click = False
			for i,_,_ in self.hovered_indices:
				el = self.layout_elements[i]
				self._callHandler(el.name, "release")
				el.onRelease()

				# Need to be rebuilt
				el_indices_to_rebuild.append(i)
		# WINDOW events
		if event.type == sdl2.SDL_WINDOWEVENT:
			if event.window.event == sdl2.SDL_WINDOWEVENT_FOCUS_GAINED:
				self.is_window_focused = True
			if event.window.event == sdl2.SDL_WINDOWEVENT_FOCUS_LOST:
				self.is_window_focused = False

		# Textinput handling
		if text_input is not None:
			for i, el in enumerate(self.layout_elements):
				if el.onTextInput(text_input):
					el_indices_to_rebuild.append(i)

		# Cursor changing
		if self.text_input_hovered:
			changeCursor(TEXT)
		else:
			changeCursor(ARROW)

		# Rebuild if necessary
		if len(el_indices_to_rebuild) > 0:
			for i in el_indices_to_rebuild:
				self._buildElement(i)

	def _findHoveredElements(self, X, Y):
		"""
		Given the coordinates of the mouse, find which rects
		are hovered.
		"""
		hovered_indices = []
		for i, rect in enumerate(self.layout_rects):
			if rect.isOver(X, Y):
				hovered_indices.append((i, X - rect.x, Y - rect.y))

		return hovered_indices

	def _callHandler(self, element_name, event_type, extra_params=None):
		if element_name in self.handlers and event_type in self.handlers[element_name]:
			params = self.handlers[element_name][event_type][1]
			if params is not None:
				self.handlers[element_name][event_type][0](params)
			else:
				if extra_params is not None:
					self.handlers[element_name][event_type][0](extra_params)
				else:
					self.handlers[element_name][event_type][0]()
