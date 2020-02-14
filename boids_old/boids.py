from .boid import Boid


class Boids:
    def __init__(self, count, borders):
        self.boids = list()
        self.borders = borders

        self.initialize(count)

    def initialize(self, count):
        for _ in range(count):
            self.boids.append(Boid(self.boids, self.borders))

    def update(self, dt):
        for boid in self.boids:
            boid.update(dt)

    def draw(self):
        for boid in self.boids:
            boid.draw()
