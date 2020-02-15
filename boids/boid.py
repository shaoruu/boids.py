import math
import random
import numpy as np

from pyrr import vector, vector3
from three.geometry import ConeGeometry
from three.material import SurfaceLightMaterial
from three.core import Mesh

DEFAULT_VELOCITY = 1
MAX_SPEED = 3
MAX_FORCE = 3
EPSILON = 0.01

DESIRED_SEPARATION = 10
NEIGHBOR_DIST = 20

SEPARATION_WEIGHT = 1.5
ALIGNMENT_WEIGHT = 1
COHESION_WEIGHT = 1


class Boid:
    def __init__(self, scene, boids, borders, radius=.2, height=.4):
        self.scene = scene
        self.borders = borders

        self.others = boids

        self.acceleration = vector3.create(0, 0, 0)
        self.velocity = vector3.create(
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY),
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY),
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY)
        )

        self.geometry = ConeGeometry(radius=radius, height=height)
        self.material = SurfaceLightMaterial(color=[.5, .5, 1])
        self.mesh = Mesh(self.geometry, self.material)
        self.transform = self.mesh.transform

        self.scene.add(self.mesh)

    def update(self, dt):
        self.velocity = self.velocity + self.acceleration
        self.velocity = vector3.create(
            *[MAX_FORCE if n >= MAX_SPEED else n for n in self.velocity])
        dx, dy, dz = self.velocity * dt

        # UPDATE ROTATION
        x, y, z = self.transform.getPosition()
        self.transform.lookAt(x + dx, y + dy, z + dz)

        # UPDATE POSITION
        self.transform.translate(dx, dy, dz)
        self.acceleration = vector3.create(0, 0, 0)

        bw = self.borders.width
        bh = self.borders.height
        bd = self.borders.depth

        normalized = vector.normalize(self.velocity)
        normalized = normalized * math.pi

        if self.position[0] > bw / 2:
            self.position[0] = bw / 2 - EPSILON
            self.velocity[0] = -self.velocity[0]
        elif self.position[0] < -bw / 2:
            self.position[0] = -bw / 2 + EPSILON
            self.velocity[0] = -self.velocity[0]

        if self.position[1] > bh / 2:
            self.position[1] = bh / 2 - EPSILON
            self.velocity[1] = -self.velocity[1]
        elif self.position[1] < -bh / 2:
            self.position[1] = -bh / 2 + EPSILON
            self.velocity[1] = -self.velocity[1]

        if self.position[2] > bd / 2:
            self.position[2] = bd / 2 - EPSILON
            self.velocity[2] = -self.velocity[2]
        elif self.position[2] < -bd / 2:
            self.position[2] = -bd / 2 + EPSILON
            self.velocity[2] = -self.velocity[2]
