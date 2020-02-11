from .boid import Boid


class Boids:
    def __init__(self, count):
        self.boids = list()

        self.initialize(count)

    def initialize(self, count):
        for _ in range(count):
            self.boids.append(Boid(self))

    def draw(self):
        for boid in self.boids:
            boid.draw()
