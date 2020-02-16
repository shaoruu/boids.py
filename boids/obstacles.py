import random

from .obstacle import Obstacle


class Obstacles:
    def __init__(self, scene, count, dimension, borders):
        self.scene = scene
        self.borders = borders

        self.dimension = dimension

        self.initialize(count, dimension)

    def initialize(self, count, dimension):
        self.obstacles = []
        bw, bh, bd = self.borders.get_dimensions()

        for _ in range(count):
            position = [
                random.uniform(-bw/2+dimension/2, bw/2-dimension/2),
                random.uniform(-bh/2+dimension/2, bh/2-dimension/2),
                random.uniform(-bd/2+dimension/2, bd/2-dimension/2),
            ]

            self.obstacles.append(
                Obstacle(self.scene, *position, self.dimension))

    def get_obstacles(self):
        return self.obstacles
