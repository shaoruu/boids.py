from .boid import Boid
from .octree import Octree


ORIGIN = (0, 0, 0)


class Boids:
    def __init__(self, scene, count, borders):
        self.boids = list()

        self.scene = scene
        self.borders = borders

        self.initialize(count)

    def initialize(self, count):
        for _ in range(count):
            self.boids.append(Boid(self.scene, self.borders))

    def update(self, dt):
        octree = Octree(*self.borders.get_max_coords(), *
                        self.borders.get_min_coords(), ORIGIN)

        for boid in self.boids:
            octree.add_item(boid, boid.position)

        for boid in self.boids:
            boid.update(dt, octree)

    def draw(self):
        for boid in self.boids:
            boid.draw()
