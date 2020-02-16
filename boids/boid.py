import math
import random
import numpy as np

from pyrr import vector, vector3
from three.geometry import ConeGeometry
from three.material import SurfaceLightMaterial
from three.core import Mesh


DEFAULT_VELOCITY = 2
MAX_SPEED = 2
MAX_FORCE = 4
EPSILON = 0.05

DESIRED_SEPARATION = 4
NEIGHBOR_DIST = 6

SEPARATION_GAIN = 0.6
ALIGNMENT_GAIN = 1.8
COHESION_GAIN = 0.6
BOUND_STRENGTH = 3
BORDER_DIST = .5

BOID_RANGE = 5


class Boid:
    def __init__(self, scene, borders, radius=.2, height=.4):
        self.scene = scene
        self.borders = borders

        self.position = vector3.create(0.0, 0.0, 0.0)

        self.acceleration = vector3.create(0.0, 0.0, 0.0)
        # self.velocity = vector3.create(1, 0, 0)
        self.velocity = vector3.create(
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY),
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY),
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY)
        )

        self.geometry = ConeGeometry(radius=radius, height=height)
        self.material = SurfaceLightMaterial(color=[.5, .5, 1])
        self.mesh = Mesh(self.geometry, self.material)
        self.transform = self.mesh.transform

        bw, bh, bd = self.borders.get_dimensions()
        self.transform.translate(
            random.uniform(-bw/2+EPSILON, bw/2-EPSILON),
            random.uniform(-bh/2+EPSILON, bh/2-EPSILON),
            random.uniform(-bd/2+EPSILON, bd/2-EPSILON)
        )

        self.scene.add(self.mesh)

    def separate(self, octree):
        steer = vector3.create(0.0, 0.0, 0.0)

        boids = octree.find_within_range(
            self.position, DESIRED_SEPARATION, "cube")
        boids = [boid[0][1] for boid in boids]

        if len(boids) <= 1:
            return steer

        for boid in boids:
            if boid is self:
                # TODO: check angle
                continue

            offset = self.position - boid.position
            steer -= offset

        steer *= SEPARATION_GAIN

        return steer

    def align(self, octree):
        total = vector3.create(0.0, 0.0, 0.0)

        boids = octree.find_within_range(
            self.position, DESIRED_SEPARATION, "cube")
        boids = [boid[0][1] for boid in boids]

        if len(boids) <= 1:
            return total

        for boid in boids:
            if boid is self:
                continue

            total += boid.velocity

        total /= len(boids)
        total -= self.velocity

        self.apply_limit(total, MAX_FORCE)

        return total / (15 / ALIGNMENT_GAIN)

    def cohesion(self, octree):
        total = vector3.create(0.0, 0.0, 0.0)

        boids = octree.find_within_range(
            self.position, DESIRED_SEPARATION, "cube")
        boids = [boid[0][1] for boid in boids]

        if len(boids) <= 1:
            return total

        for boid in boids:
            if boid is self:
                continue

            total += boid.position

        total /= len(boids)
        total *= COHESION_GAIN

        self.apply_limit(total, MAX_FORCE)

        return total

    def bound(self):
        bw, bh, bd = self.borders.get_dimensions()

        steer = vector3.create(0.0, 0.0, 0.0)
        # bounding_force = .05 * BOUND_STRENGTH
        bounding_force = BOUND_STRENGTH

        x, y, z = self.position

        if x > bw/2 - BORDER_DIST:
            diff = abs(x - bw/2)
            steer[0] = -bounding_force * diff
        if x < -bw/2 + BORDER_DIST:
            diff = abs(x - bw/2)
            steer[0] = bounding_force * diff

        if y > bh/2 - BORDER_DIST:
            diff = abs(y - bh/2)
            steer[1] = -bounding_force * diff
        if y < -bh/2 + BORDER_DIST:
            diff = abs(y - bh/2)
            steer[1] = bounding_force * diff

        if z > bd/2 - BORDER_DIST:
            diff = abs(z - bd/2)
            steer[2] = -bounding_force * diff
        if z < -bd/2 + BORDER_DIST:
            diff = abs(z - bd/2)
            steer[2] = bounding_force * diff

        # self.apply_limit(steer, MAX_FORCE)

        return steer

    def apply_limit(self, v, max):
        if vector.length(v) > max:
            v = vector.normalize(v)
            v *= max

    def apply_force(self, force):
        self.acceleration = self.acceleration + force

    def flock(self, octree):
        sep = self.separate(octree)
        self.apply_force(sep)

        ali = self.align(octree)
        self.apply_force(ali)

        coh = self.cohesion(octree)
        self.apply_force(coh)

        bound = self.bound()
        self.apply_force(bound)

    def update(self, dt, octree):
        self.flock(octree)

        self.velocity = self.velocity + self.acceleration
        self.apply_limit(self.velocity, MAX_SPEED)
        dx, dy, dz = self.velocity * dt

        # UPDATE ROTATION
        x, y, z = self.transform.getPosition()
        if dx+dy+dz != 0.0:
            self.transform.lookAt(x + dx, y + dy, z + dz)
            self.transform.rotateX(-math.pi/2, 1)  # fix rotation

        # UPDATE POSITION
        self.transform.translate(dx, dy, dz)
        self.acceleration = vector3.create(0.0, 0.0, 0.0)

        x, y, z = self.transform.getPosition()
        self.position = vector3.create(x, y, z)

        # if self.position[0] > bw / 2:
        #     self.position[0] = -bw / 2 + EPSILON
        # elif self.position[0] < -bw / 2:
        #     self.position[0] = bw / 2 - EPSILON

        # if self.position[1] > bh / 2:
        #     self.position[1] = -bh / 2 + EPSILON
        # elif self.position[1] < -bh / 2:
        #     self.position[1] = bh / 2 - EPSILON

        # if self.position[2] > bd / 2:
        #     self.position[2] = -bd / 2 + EPSILON
        # elif self.position[2] < -bd / 2:
        #     self.position[2] = bd / 2 - EPSILON

        # if self.position[0] > bw / 2:
        #     self.position[0] = bw / 2 - EPSILON
        #     self.velocity[0] = -self.velocity[0]
        # elif self.position[0] < -bw / 2:
        #     self.position[0] = -bw / 2 + EPSILON
        #     self.velocity[0] = -self.velocity[0]

        # if self.position[1] > bh / 2:
        #     self.position[1] = bh / 2 - EPSILON
        #     self.velocity[1] = -self.velocity[1]
        # elif self.position[1] < -bh / 2:
        #     self.position[1] = -bh / 2 + EPSILON
        #     self.velocity[1] = -self.velocity[1]

        # if self.position[2] > bd / 2:
        #     self.position[2] = bd / 2 - EPSILON
        #     self.velocity[2] = -self.velocity[2]
        # elif self.position[2] < -bd / 2:
        #     self.position[2] = -bd / 2 + EPSILON
        #     self.velocity[2] = -self.velocity[2]

        # x, y, z = self.position
        # self.transform.setPosition(x, y, z)
