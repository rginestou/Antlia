from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

import os
import sys
import ctypes
import numpy
from numpy import array

os.environ["PYSDL2_DLL_PATH"] = "lib/"
try:
	import sdl2
	from sdl2 import video
except ImportError:
	import traceback
	traceback.print_exc()
	sys.exit(1)

class Renderer:
	"""
	The Renderer initializes an OpenGL context
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
		self.window_width = self.params["resolution"]["width"]
		self.window_height = self.params["resolution"]["height"]

		# OpenGL specific
		self.vertex_data = []
		self.shader_program = None
		self.VAO = None
		self.VBO = None

	def createWindow(self):
		# Create the window context
		if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
			print(sdl2.SDL_GetError())
			return -1

		self.window = sdl2.SDL_CreateWindow(self.params["name"].encode(),
					   sdl2.SDL_WINDOWPOS_UNDEFINED,
					   sdl2.SDL_WINDOWPOS_UNDEFINED,
					   self.window_width,
					   self.window_height,
					   sdl2.SDL_WINDOW_OPENGL)
		if not self.window:
			print(sdl2.SDL_GetError())
			return -1

		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 3)
		video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
			video.SDL_GL_CONTEXT_PROFILE_CORE)
		self.context = sdl2.SDL_GL_CreateContext(self.window)

		# Basic initialization
		self._initialize()
		self.is_window_created = True

		# look for events
		self._loopForEvents()

	def update(self, vertex_data):
		self.vertex_data = vertex_data
		self.need_update = True

	def quit(self):
		sdl2.SDL_GL_DeleteContext(self.context)
		sdl2.SDL_DestroyWindow(self.window)
		sdl2.SDL_Quit()

	def _refresh(self):
		"""
		Draws the GUI when it needs to be updated
		"""
		glClearColor(1.0, 1.0, 1.0, 1.0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# Active shader program
		glUseProgram(self.shader_program)
		glUniformMatrix4fv(self.viewportUniform, 1, GL_FALSE, self.viewportMatrix)


		try:
			# Activate the array of elements
			glBindVertexArray(self.VAO)

			# Draw on the screen
			glDrawArrays(GL_TRIANGLES, 0, self.vertex_data_length)
		finally:
			glBindVertexArray(0)
			glUseProgram(0)

		sdl2.SDL_GL_SwapWindow(self.window)

	def _initialize(self):
		# Load the shaders
		with open("sources/shader.vertex", "r") as f:
			vertexShader = shaders.compileShader(f.read(), GL_VERTEX_SHADER)

		with open("sources/shader.fragment", "r") as f:
			fragmentShader = shaders.compileShader(f.read(), GL_FRAGMENT_SHADER)

		self.shader_program = shaders.compileProgram(vertexShader, fragmentShader)

	def _updateBuffer(self):
		# Core OpenGL requires that at least one OpenGL vertex array be bound
		self.VAO = glGenVertexArrays(1)
		glBindVertexArray(self.VAO)

		# Need VBO for vertices and colors
		self.VBO = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER, self.vertex_data.nbytes, self.vertex_data,
			GL_STATIC_DRAW)
		self.vertex_data_length = int(self.vertex_data.nbytes / 28)

		# Enable array and set up data
		positionAttrib = glGetAttribLocation(self.shader_program, 'position')
		colorAttrib = glGetAttribLocation(self.shader_program, 'color')

		# Set uniform
		self.viewportMatrix = numpy.zeros((4,4), dtype=numpy.float32)
		self.viewportMatrix[0,0] = 2.0 / self.window_width;
		self.viewportMatrix[1,1] = -2.0 / self.window_height
		self.viewportMatrix[3,0] = -1.0; self.viewportMatrix[3,1] = 1.0
		self.viewportMatrix[3,3] = 1
		self.viewportUniform = glGetUniformLocation(self.shader_program, 'viewport')

		glEnableVertexAttribArray(0)
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(positionAttrib, 3, GL_FLOAT, GL_FALSE, 4 * 7,
			None)
		glVertexAttribPointer(colorAttrib, 3, GL_FLOAT, GL_FALSE, 4 * 7,
			ctypes.c_void_p(12))

		# Finished
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindVertexArray(0)

	def _loopForEvents(self):
		event = sdl2.SDL_Event()
		while True:
			# Look at the event queue
			while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
				self.onEvent(event)

			# Look for layout changes
			if self.need_update:
				self._updateBuffer()
				self._refresh()
				self.need_update = False
			sdl2.SDL_Delay(5)
