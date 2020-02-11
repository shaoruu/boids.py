from pyglet.gl import *


class Boid:
    def __init__(self, boids, size=.2, height=.4):
        self.boids = boids
        self.size = size  # base cross width
        self.height = height

        self.position = (0, 0, 0)
        self.rotation = (0, 0, 0)

    def draw(self):
        x, y, z = self.position
        size = self.size
        height = self.height

        vertices = (
            (x, y, z+size/2),
            (x+size/2, y, z),
            (x, y, z-size/2),
            (x-size/2, y, z),
            (x, y+height, z)
        )

        edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3)
        )

        glLineWidth(2.0)
        glBegin(GL_LINES)
        glRotatef(1, 3, 1, 1)
        for edge in edges:
            for vertex in edge:
                glVertex3f(*vertices[vertex])
        glEnd()
