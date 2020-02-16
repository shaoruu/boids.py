from three.core import Mesh
from three.geometry import BoxGeometry
from three.material import SurfaceLightMaterial
from pyrr import vector3

from .config import BLOCK_WIDTH

OBSTACLE_COLOR = [1.0, 1.0, 1.0]
OBSTACLE_ALPHA = .15


class Obstacle:
    def __init__(self, scene, x, y, z, dimension):
        self.scene = scene

        self.position = vector3.create(x, y, z)

        self.dimension = dimension

        self.generate()

    def generate(self):
        geo = BoxGeometry(self.dimension * BLOCK_WIDTH,
                          self.dimension * BLOCK_WIDTH, self.dimension * BLOCK_WIDTH)
        mat = SurfaceLightMaterial(color=OBSTACLE_COLOR, alpha=OBSTACLE_ALPHA)
        mesh = Mesh(geo, mat)

        x, y, z = self.position
        mesh.transform.translate(x, y, z)

        self.scene.add(mesh)

    def get_dimensions(self):
        # TODO: FIX THIS UGLY CODE
        return [self.dimension * BLOCK_WIDTH, self.dimension * BLOCK_WIDTH, self.dimension * BLOCK_WIDTH]
