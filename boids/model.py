from pyglet.gl import *


class Model:
    def __init__(self, width, height, depth, block_dimension=.1):
        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()

        self.width = width
        self.height = height
        self.depth = depth

        self.block_dimension = block_dimension

        self._initialize()

    def _initialize(self):
        pass

    def draw(self):
        # BORDERS
        # X
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                mapped_y = self.height / 2 * i
                mapped_z = self.depth / 2 * j

                self.draw_box_at(position=(0, mapped_y, mapped_z), dimensions=(
                    self.width, self.block_dimension, self.block_dimension))

        # Y
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                mapped_x = self.width / 2 * i
                mapped_z = self.depth / 2 * j

                self.draw_box_at(position=(mapped_x, 0, mapped_z), dimensions=(
                    self.block_dimension, self.height, self.block_dimension))

        # Z
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                mapped_x = self.width / 2 * i
                mapped_y = self.height / 2 * j

                self.draw_box_at(position=(mapped_x, mapped_y, 0), dimensions=(
                    self.block_dimension, self.block_dimension, self.depth))

    def draw_box_at(self, position, dimensions):
        x, y, z = position
        w, h, d = dimensions

        vertices = (
            (x-w/2, y-h/2, z-d/2),
            (x+w/2, y-h/2, z-d/2),
            (x-w/2, y+h/2, z-d/2),
            (x+w/2, y+h/2, z-d/2),
            (x-w/2, y-h/2, z+d/2),
            (x+w/2, y-h/2, z+d/2),
            (x-w/2, y+h/2, z+d/2),
            (x+w/2, y+h/2, z+d/2),
        )

        edges = (
            (0, 1),
            (2, 3),
            (6, 7),
            (4, 5),
            (0, 2),
            (1, 3),
            (5, 7),
            (4, 6),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7)
        )

        glLineWidth(2.0)
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3f(*vertices[vertex])
        glEnd()
