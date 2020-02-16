import pygame

from tkinter import *
from three.core import Base, Renderer, Scene, FirstPersonController
from three.cameras import PerspectiveCamera
from three.lights import AmbientLight, DirectionalLight

from .borders import Borders
from .boids import Boids


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# BOIDS_COUNT = 1
BOIDS_COUNT = 30

BOX_DIM = 80


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
        self.camera.transform.setPosition(0, 0, BOX_DIM / 2)
        self.camera.transform.lookAt(0, 0, 0)
        self.controls = FirstPersonController(self.input, self.camera, BOX_DIM)

        self.borders = Borders(self.scene, BOX_DIM, BOX_DIM, BOX_DIM)
        self.boids = Boids(self.scene, BOIDS_COUNT, self.borders)

        self.init_ui()

    def init_ui(self):
        self.master = Tk()

        self.speed_slider = Scale(
            self.master, from_=1, to=10, orient=HORIZONTAL, label='Speed')
        self.speed_slider.pack()
        self.speed_slider.set(5)

        self.force_slider = Scale(
            self.master, from_=1, to=10, orient=HORIZONTAL, label='Force')
        self.force_slider.pack()
        self.force_slider.set(5)

        self.separation_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Separation')
        self.separation_slider.pack()
        self.separation_slider.set(5)

        self.alignment_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Alignment')
        self.alignment_slider.pack()
        self.alignment_slider.set(5)

        self.cohesion_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Cohesion')
        self.cohesion_slider.pack()
        self.cohesion_slider.set(5)

        self.bound_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Bound Force')
        self.bound_slider.pack()
        self.bound_slider.set(5)

        self.neighbor_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Neighbor Dist.')
        self.neighbor_slider.pack()
        self.neighbor_slider.set(5)

        self.bound_dist_slider = Scale(
            self.master, from_=0, to=10, orient=HORIZONTAL, label='Bound Dist.')
        self.bound_dist_slider.pack()
        self.bound_dist_slider.set(5)

    def update(self):
        self.check_resize()

        self.master.update()

        values = {
            'speed': self.speed_slider.get(),
            'force': self.force_slider.get(),
            'separation': self.separation_slider.get() / 5,
            'alignment': self.alignment_slider.get() / 5,
            'cohesion': self.cohesion_slider.get() / 5,
            'bound': self.bound_slider.get() / 5,
            'neighbor': self.neighbor_slider.get(),
            'bound_dist': self.bound_dist_slider.get(),
        }

        self.controls.update()
        self.boids.update(1/60, values)

        self.renderer.render(self.scene, self.camera)

    def check_resize(self):
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio(size["width"]/size["height"])
            self.renderer.setViewportSize(size["width"], size["height"])
