import pygame

from tkinter import *
from three.core import Base, Renderer, Scene, FirstPersonController
from three.cameras import PerspectiveCamera
from three.lights import AmbientLight, DirectionalLight

from .borders import Borders
from .obstacles import Obstacles
from .boids import Boids
from .config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BOIDS_COUNT, BOX_DIM,
    OBSTACLE_DIM, BLOCK_WIDTH, DEFAULT_SPEED, DEFAULT_FORCE,
    DEFAULT_ALIGNMENT, DEFAULT_SEPARATION, DEFAULT_COHESION,
    DEFAULT_BOUND, DEFAULT_AVOID, DEFAULT_NEIGHBOR_DIST,
    OBSTACLE_COUNT
)


class Main(Base):
    def initialize(self):
        self.setWindowTitle('Flocking')
        self.setWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.renderer = Renderer()
        self.renderer.setViewportSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.renderer.setClearColor(0, 0, 0)

        self.scene = Scene()

        self.scene.add(AmbientLight(strength=0.25))
        self.scene.add(DirectionalLight(direction=[-1, -1, -1]))

        self.camera = PerspectiveCamera(aspectRatio=WINDOW_WIDTH/WINDOW_HEIGHT)
        self.camera.transform.setPosition(0, 0, BOX_DIM / 3)
        self.camera.transform.lookAt(0, 0, 0)
        self.controls = FirstPersonController(self.input, self.camera, BOX_DIM)

        self.borders = Borders(self.scene, BOX_DIM, BOX_DIM, BOX_DIM)
        self.obstacles = Obstacles(
            self.scene, OBSTACLE_COUNT, OBSTACLE_DIM, self.borders)

        self.boids1 = Boids(self.scene, BOIDS_COUNT,
                            self.borders, self.obstacles, [.5, .5, 1])
        self.boids2 = Boids(self.scene, BOIDS_COUNT,
                            self.borders, self.obstacles, [.7, .7, .2])
        self.boids3 = Boids(self.scene, BOIDS_COUNT,
                            self.borders, self.obstacles, [.2, .2, .6])

        self.init_ui()

    def init_ui(self):
        self.master = Tk()

        self.speed_slider = Scale(
            self.master, from_=1, to=10, orient=HORIZONTAL, label='Speed')
        self.speed_slider.pack()
        self.speed_slider.set(DEFAULT_SPEED)

        self.force_slider = Scale(
            self.master, from_=1, to=10, orient=HORIZONTAL, label='Force')
        self.force_slider.pack()
        self.force_slider.set(DEFAULT_FORCE)

        self.separation_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Separation')
        self.separation_slider.pack()
        self.separation_slider.set(DEFAULT_SEPARATION)

        self.alignment_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Alignment')
        self.alignment_slider.pack()
        self.alignment_slider.set(DEFAULT_ALIGNMENT)

        self.cohesion_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Cohesion')
        self.cohesion_slider.pack()
        self.cohesion_slider.set(DEFAULT_COHESION)

        self.bound_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Bound Force')
        self.bound_slider.pack()
        self.bound_slider.set(DEFAULT_BOUND)

        self.avoid_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label="Avoidance Force")
        self.avoid_slider.pack()
        self.avoid_slider.set(DEFAULT_AVOID)

        self.neighbor_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Neighbor Dist.')
        self.neighbor_slider.pack()
        self.neighbor_slider.set(DEFAULT_NEIGHBOR_DIST)

        self.bound_dist_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Bound Dist.')
        self.bound_dist_slider.pack()
        self.bound_dist_slider.set(5)

        self.avoid_dist_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Avoidance Dist.')
        self.avoid_dist_slider.pack()
        self.avoid_dist_slider.set(5)

    def update(self):
        self.check_resize()

        self.master.update()

        values = {
            'speed': self.speed_slider.get(),
            'force': self.force_slider.get() * 5,
            'separation': self.separation_slider.get() / 100,
            'alignment': self.alignment_slider.get() / 100,
            'cohesion': self.cohesion_slider.get() / 100,
            'bound': self.bound_slider.get() / 5,
            'avoid': self.avoid_slider.get() / 100,
            'neighbor': self.neighbor_slider.get(),
            'bound_dist': self.bound_dist_slider.get() / 30,
            'avoidance_dist': self.avoid_dist_slider.get() / 30
        }

        self.controls.update()
        self.boids1.update(1/60, values)
        self.boids2.update(1/60, values)
        self.boids3.update(1/60, values)

        self.renderer.render(self.scene, self.camera)

    def check_resize(self):
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio(size["width"]/size["height"])
            self.renderer.setViewportSize(size["width"], size["height"])
