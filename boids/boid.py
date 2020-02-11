import math
import random
import numpy as np

from pyrr import vector, vector3
from pyglet.gl import *


MAX_SPEED = 3
MAX_FORCE = 3
EPSILON = 0.01

SEPARATION_WEIGHT = 1.5
ALIGNMENT_WEIGHT = 1
COHESION_WEIGHT = 1


class Boid:
    def __init__(self, boids, borders, size=.2, height=.4):
        self.others = boids
        self.size = size  # base cross width
        self.height = height

        self.borders = borders

        self.position = vector3.create(0, 0, 0)
        self.rotation = vector3.create(45, 45, 45)

        self.acceleration = vector3.create(0, 0, 0)
        self.velocity = vector3.create(
            random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01))

    def separate(self):
        desiredseparation = 10  # unit
        steer = vector3.create(0, 0, 0)
        count = 0

        for boid in self.others:
            if boid is self:
                continue

            _, d = vector.length([self.position, boid.position])

            if d > 0 and d < desiredseparation:
                diff = self.position - boid.position
                diff = vector.normalize(diff)
                diff = diff / d
                steer = steer + diff
                count += 1

        if count > 0:
            steer = steer / count

        if vector.length(steer) > 0:
            steer = vector.normalize(steer)
            steer = steer * MAX_SPEED
            steer = steer - self.velocity
            steer = vector3.create(
                *[MAX_FORCE if n >= MAX_FORCE else n for n in steer])

        return steer

    def align(self):
        neighbordist = 20
        total = vector3.create(0, 0, 0)
        count = 0

        for boid in self.others:
            if boid is self:
                continue

            _, d = vector.length([self.position, boid.position])

            if d > 0 and d < neighbordist:
                total = total + boid.velocity
                count = count + 1

        if count > 0:
            total = total / count
            total = vector.normalize(total)
            total = total * MAX_SPEED
            steer = total - self.velocity
            steer = vector3.create(
                *[MAX_FORCE if n >= MAX_FORCE else n for n in steer])
            return steer
        return vector3.create(0, 0, 0)

    def cohesion(self):
        neighbordist = 20
        total = vector3.create(0, 0, 0)
        count = 0

        for boid in self.others:
            if boid is self:
                continue

            _, d = vector.length([self.position, boid.position])

            if d > 0 and d < neighbordist:
                total = total + boid.position
                count = count + 1

        if count > 0:
            total = total / count
            return self.seek(total)
        return vector3.create(0, 0, 0)

    def seek(self, target):
        desired = target - self.position
        desired = vector.normalize(desired)
        desired = desired * MAX_SPEED
        steer = desired - self.velocity
        steer = vector3.create(
            *[MAX_FORCE if n >= MAX_FORCE else n for n in steer])
        return steer

    def apply_force(self, force):
        self.acceleration = self.acceleration + force

    def flock(self):
        sep = self.separate()
        ali = self.align()
        coh = self.cohesion()

        sep = sep * SEPARATION_WEIGHT
        ali = ali * ALIGNMENT_WEIGHT
        coh = coh * COHESION_WEIGHT

        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def update(self, dt):
        self.flock()

        self.velocity = self.velocity + self.acceleration
        self.velocity = vector3.create(
            *[MAX_FORCE if n >= MAX_SPEED else n for n in self.velocity])

        self.position = self.position + self.velocity * dt
        self.acceleration = vector3.create(0, 0, 0)

        bw = self.borders.width
        bh = self.borders.height
        bd = self.borders.depth

        normalized = vector.normalize(self.velocity)
        normalized = normalized * math.pi

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

        if self.position[0] > bw / 2:
            self.position[0] = bw / 2 - EPSILON
        elif self.position[0] < -bw / 2:
            self.position[0] = -bw / 2 + EPSILON

        if self.position[1] > bh / 2:
            self.position[1] = bh / 2 - EPSILON
        elif self.position[1] < -bh / 2:
            self.position[1] = -bh / 2 + EPSILON

        if self.position[2] > bd / 2:
            self.position[2] = bd / 2 - EPSILON
        elif self.position[2] < -bd / 2:
            self.position[2] = -bd / 2 + EPSILON

    def draw(self):
        x, y, z = self.position
        rx, ry, rz = self.rotation
        size = self.size
        height = self.height

        vertices = (
            (0, 0, size/2),
            (size/2, 0, 0),
            (0, 0, -size/2),
            (-size/2, 0, 0),
            (0, height, 0)
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

        glPushMatrix()
        glLineWidth(1.0)
        # glLoadIdentity()
        glTranslatef(x, y, z)
        glRotated(rz, 0, 0, 1)
        glRotated(rx, 1, 0, 0)
        glRotated(ry, 0, 1, 0)
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3f(*vertices[vertex])
        glEnd()
        glPopMatrix()
