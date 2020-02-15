import pygame

from three.core import Base, Renderer, Scene, FirstPersonController
from three.cameras import PerspectiveCamera
from three.lights import AmbientLight, DirectionalLight

from .borders import Borders
from .boids import Boids


WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1200

BOIDS_COUNT = 10


class Main(Base):
    def initialize(self):
        self.setWindowTitle('Boids')
        self.setWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.renderer = Renderer()
        self.renderer.setViewportSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.renderer.setClearColor(0, 0, 0)

        self.scene = Scene()

        self.scene.add(AmbientLight(strength=0.25))
        self.scene.add(DirectionalLight(direction=[-1, -1, -1]))

        self.camera = PerspectiveCamera(aspectRatio=WINDOW_WIDTH/WINDOW_HEIGHT)
        self.camera.transform.setPosition(0, 0, 14)
        self.camera.transform.lookAt(0, 0, 0)
        self.controls = FirstPersonController(self.input, self.camera)

        self.borders = Borders(self.scene, 40, 40, 40)
        self.boids = Boids(self.scene, BOIDS_COUNT, self.borders)

    def update(self):
        self.check_resize()

        self.controls.update()
        self.boids.update(1/60)

        self.renderer.render(self.scene, self.camera)

    def check_resize(self):
        if self.input.resize():
            size = self.input.getWindowSize()
            self.camera.setAspectRatio(size["width"]/size["height"])
            self.renderer.setViewportSize(size["width"], size["height"])
