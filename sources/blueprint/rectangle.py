from .primitive import Primitive
from .vertex import Vertex

class Rectangle(Primitive):
	"""
	"""
	def __init__(self, x, y, width, height):
		super(Rectangle, self).__init__()
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.vertices = [Vertex(self.x, self.y),
						Vertex(self.x + self.width, self.y),
						Vertex(self.x + self.width, self.y + self.height),
						Vertex(self.x, self.y),
						Vertex(self.x + self.width, self.y + self.height),
						Vertex(self.x, self.y + self.height)]
