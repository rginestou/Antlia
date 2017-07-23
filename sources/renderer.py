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
	def __init__(self, layout, onEvent):
		self.layout = layout
		self.onEvent = onEvent

		# OpenGL specific
		self.shaderProgram = None
		self.VAO = None
		self.VBO = None

	def createWindow(self):
		# Create the window context
		if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
			print(sdl2.SDL_GetError())
			return -1

		self.window = sdl2.SDL_CreateWindow(b"OpenGL demo",
					   sdl2.SDL_WINDOWPOS_UNDEFINED,
					   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
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

		self.refresh()

		# look for events
		self._loopForEvents()

	def refresh(self):
		"""
		Draws the GUI when it needs to be updated
		"""
		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# Active shader program
		glUseProgram(self.shaderProgram)

		try:
			# Activate the array of elements
			glBindVertexArray(self.VAO)

			# Draw on the screen
			glDrawArrays(GL_TRIANGLE_STRIP, 0, 3)
		finally:
			glBindVertexArray(0)
			glUseProgram(0)

		sdl2.SDL_GL_SwapWindow(self.window)

	def quit(self):
		sdl2.SDL_GL_DeleteContext(self.context)
		sdl2.SDL_DestroyWindow(self.window)
		sdl2.SDL_Quit()

	def _initialize(self):
		# Load the shaders
		with open("sources/shader.vertex", "r") as f:
			vertexShader = shaders.compileShader(f.read(), GL_VERTEX_SHADER)

		with open("sources/shader.fragment", "r") as f:
			fragmentShader = shaders.compileShader(f.read(), GL_FRAGMENT_SHADER)

		self.shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)

		vertexData = numpy.array([
			 # X,    Y,    Z     R,   G,   B,   A
			 0.0,  0.0,  0.0,  1.0, 1.0, 0.0, 1.0,
			 1.0,  0.0,  0.0,  1.0, 0.0, 0.0, 1.0,
			 1.0,  1.0,  0.0,  1.0, 0.0, 0.0, 1.0,
			 0.0,  1.0,  0.0,  1.0, 0.0, 0.0, 1.0,
		], dtype=numpy.float32)

		# Core OpenGL requires that at least one OpenGL vertex array be bound
		self.VAO = glGenVertexArrays(1)
		glBindVertexArray(self.VAO)

		# Need VBO for triangle vertices and colors
		self.VBO = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData,
			GL_STATIC_DRAW)

		# Enable array and set up data
		positionAttrib = glGetAttribLocation(self.shaderProgram, 'position')
		colorAttrib = glGetAttribLocation(self.shaderProgram, 'color')

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
			while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
				self.onEvent(event)
			sdl2.SDL_Delay(10)
