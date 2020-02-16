import random

from .boid import Boid
from .octree import Octree


ORIGIN = (0, 0, 0)


class Boids:
    def __init__(self, scene, count, borders, obstacles, color):
        self.boids = list()

        self.scene = scene
        self.borders = borders
        self.obstacles = obstacles

        self.initialize(count, color)

    def initialize(self, count, color):
        bw, bh, bd = self.borders.get_dimensions()
        init_pos = (random.uniform(-bw/2, bw/2),
                    random.uniform(-bh/2, bh/2), random.uniform(-bd/2, bd/2))

        for _ in range(count):
            self.boids.append(
                Boid(self.scene, init_pos, self.borders, self.obstacles, color))

    def update(self, dt, values):
        octree = Octree(*self.borders.get_max_coords(), *
                        self.borders.get_min_coords(), ORIGIN)

        for boid in self.boids:
            octree.add_item(boid, boid.position)

        for boid in self.boids:
            boid.update(dt, octree, values)

    def draw(self):
        for boid in self.boids:
            boid.draw()
