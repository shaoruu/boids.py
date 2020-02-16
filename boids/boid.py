import math
import random
import numpy as np

from pyrr import vector, vector3
from three.geometry import ConeGeometry
from three.material import SurfaceLightMaterial
from three.core import Mesh


DEFAULT_VELOCITY = 2
MAX_FORCE = 4
EPSILON = 0.05

DESIRED_SEPARATION = 4
NEIGHBOR_DIST = 6

BOUND_STRENGTH = 3
BORDER_DIST = .5

BOID_RANGE = 5


class Boid:
    def __init__(self, scene, init_pos, borders, obstacles, color, radius=.2, height=.4):
        self.scene = scene
        self.borders = borders
        self.obstacles = obstacles

        self.position = vector3.create(*init_pos)

        self.acceleration = vector3.create(0.0, 0.0, 0.0)
        # self.velocity = vector3.create(1, 0, 0)
        self.velocity = vector3.create(
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY),
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY),
            random.uniform(-DEFAULT_VELOCITY, DEFAULT_VELOCITY)
        )

        self.geometry = ConeGeometry(radius=radius, height=height)
        self.material = SurfaceLightMaterial(color=color)
        self.mesh = Mesh(self.geometry, self.material)
        self.transform = self.mesh.transform

        self.transform.translate(*self.position)

        self.scene.add(self.mesh)

    def separate(self, octree, gain):
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

        steer *= gain

        return steer

    def align(self, octree, gain, neighbor_dist):
        total = vector3.create(0.0, 0.0, 0.0)

        boids = octree.find_within_range(
            self.position, neighbor_dist, "cube")
        boids = [boid[0][1] for boid in boids]

        if len(boids) <= 1:
            return total

        for boid in boids:
            if boid is self:
                continue

            total += boid.velocity

        total /= len(boids)
        # total -= self.velocity
        total *= gain

        return total

    def cohesion(self, octree, gain, neighbor_dist):
        total = vector3.create(0.0, 0.0, 0.0)

        boids = octree.find_within_range(
            self.position, neighbor_dist, "cube")
        boids = [boid[0][1] for boid in boids]

        if len(boids) <= 1:
            return total

        for boid in boids:
            if boid is self:
                continue

            total += boid.position

        total /= len(boids)
        total *= gain

        return total

    def bound(self, bound_strength, bound_dist):
        bw, bh, bd = self.borders.get_dimensions()

        steer = vector3.create(0.0, 0.0, 0.0)
        x, y, z = self.position

        if x > bw/2 - BORDER_DIST:
            diff = abs(x - (bw/2 - BORDER_DIST))
            steer[0] = -bound_strength * diff
        elif x < -bw/2 + BORDER_DIST:
            diff = abs(x - (-bw/2 + BORDER_DIST))
            steer[0] = bound_strength * diff

        if y > bh/2 - BORDER_DIST:
            diff = abs(y - (bh/2 - BORDER_DIST))
            steer[1] = -bound_strength * diff
        elif y < -bh/2 + BORDER_DIST:
            diff = abs(y - (-bh/2 + BORDER_DIST))
            steer[1] = bound_strength * diff

        if z > bd/2 - BORDER_DIST:
            diff = abs(z - (bd/2 - BORDER_DIST))
            steer[2] = -bound_strength * diff
        elif z < -bd/2 + BORDER_DIST:
            diff = abs(z - (-bd/2 + BORDER_DIST))
            steer[2] = bound_strength * diff

        return steer

    def avoid(self, obstacle, avoidance, avoidance_dist):
        obs_dim = self.obstacles.dimension
        ox, oy, oz = obstacle.position

        steer = vector3.create(0.0, 0.0, 0.0)
        x, y, z = self.position

        if (x <= ox+obs_dim/2 + avoidance_dist and x >= ox-obs_dim/2 + avoidance_dist)\
                and (y <= oy+obs_dim/2 + avoidance_dist and y >= oy-obs_dim/2 + avoidance_dist)\
                and (z <= oz+obs_dim/2 + avoidance_dist and z >= oz-obs_dim/2 - avoidance_dist):
            if x > ox and x <= ox+obs_dim/2 + avoidance_dist:
                diff = abs(x - (ox+obs_dim/2))
                steer[0] = avoidance * diff
            elif x < ox and x >= ox-obs_dim/2 - avoidance_dist:
                diff = abs(x - (ox-obs_dim/2))
                steer[0] = -avoidance * diff

            if y > oy and y <= oy+obs_dim/2 + avoidance_dist:
                diff = abs(y - (oy+obs_dim/2))
                steer[1] = avoidance * diff
            elif y < oy and y >= oy-obs_dim/2 - avoidance_dist:
                diff = abs(y - (oy-obs_dim/2))
                steer[1] = -avoidance * diff

            if z > oz and z <= oz+obs_dim/2 + avoidance_dist:
                diff = abs(z - (oz+obs_dim/2))
                steer[2] = avoidance * diff
            elif z < oz and z >= oz-obs_dim/2 - avoidance_dist:
                diff = abs(z - (oz-obs_dim/2))
                steer[2] = -avoidance * diff

        return steer

    def apply_limit(self, v, max):
        if vector.length(v) > max:
            v2 = vector.normalize(v)
            v2 *= max
            a, b, c = v2
            v[0] = a
            v[1] = b
            v[2] = c

    def apply_force(self, force, max_force=math.inf, limit=True):
        if limit:
            self.apply_limit(force, max_force)
        self.acceleration = self.acceleration + force

    def flock(self, octree, values):
        max_force = values['force']
        sep_gain = values['separation']
        ali_gain = values['alignment']
        coh_gain = values['cohesion']
        bound_strength = values['bound']
        avoidance_strength = values['avoid']
        neighbor_dist = values['neighbor']
        bound_dist = values['bound_dist']
        avoidance_dist = values['avoidance_dist']

        sep = self.separate(octree, sep_gain)
        self.apply_force(sep, max_force)

        ali = self.align(octree, ali_gain, neighbor_dist)
        self.apply_force(ali, max_force)

        coh = self.cohesion(octree, coh_gain, neighbor_dist)
        self.apply_force(coh, max_force)

        bound = self.bound(bound_strength, bound_dist)
        self.apply_force(bound)

        for obstacle in self.obstacles.get_obstacles():
            avoid = self.avoid(obstacle, avoidance_strength, avoidance_dist)
            self.apply_force(avoid, max_force, limit=False)

    def update(self, dt, octree, values):
        if self.should_flock():
            self.flock(octree, values)

        self.velocity = self.velocity + self.acceleration
        self.apply_limit(self.velocity, values['speed'])
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

        # bw, bh, bd = self.borders.get_dimensions()

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

    def should_flock(self):
        return True
        # return random.uniform(0, 1) > 0.3
