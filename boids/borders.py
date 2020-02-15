from three.core import Mesh
from three.geometry import BoxGeometry
from three.material import SurfaceLightMaterial

CORNER_COLOR = [1.0, 1.0, 1.0]
BORDER_COLOR = [0.9, 0.9, 0.9]
BLOCK_WIDTH = .2


class Borders:
    def __init__(self, scene, width, height, depth):
        self.scene = scene

        self.width = width
        self.height = height
        self.depth = depth

        self.generate()

    def generate(self):
        width = self.width
        height = self.height
        depth = self.depth

        # CORNERS
        corner_geo = BoxGeometry(BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH)
        corner_mat = SurfaceLightMaterial(color=CORNER_COLOR)

        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                for k in range(-1, 2, 2):
                    mapped_x = width / 2 * i * BLOCK_WIDTH
                    mapped_y = height/2 * j * BLOCK_WIDTH
                    mapped_z = depth/2 * k * BLOCK_WIDTH

                    corner_mesh = Mesh(corner_geo, corner_mat)
                    corner_mesh.transform.translate(
                        mapped_x, mapped_y, mapped_z)

                    self.scene.add(corner_mesh)

        # EDGES
        edge_mat = SurfaceLightMaterial(color=BORDER_COLOR)

        # X
        for i in range(-1, 1, 2):
            for j in range(-1, 1, 2):
                dy = i * (height / 2) * BLOCK_WIDTH
                dz = j * (depth / 2) * BLOCK_WIDTH

                edge_geo = BoxGeometry(
                    (width-1) * BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH)
                mesh = Mesh(edge_geo, edge_mat)
                mesh.transform.translate(0, dy, dz)

                self.scene.add(mesh)

        # Y
        for i in range(-1, 1, 2):
            for j in range(-1, 1, 2):
                dx = i * width / 2 * BLOCK_WIDTH
                dz = j * depth / 2 * BLOCK_WIDTH

                edge_geo = BoxGeometry(BLOCK_WIDTH,
                                       (height-1) * BLOCK_WIDTH, BLOCK_WIDTH)
                mesh = Mesh(edge_geo, edge_mat)
                mesh.transform.translate(dx, 0, dz)

                self.scene.add(mesh)

        # Z
        for i in range(-1, 1, 2):
            for j in range(-1, 1, 2):
                dx = i * width / 2 * BLOCK_WIDTH
                dy = j * height / 2 * BLOCK_WIDTH

                edge_geo = BoxGeometry(BLOCK_WIDTH, BLOCK_WIDTH,
                                       (depth-1) * BLOCK_WIDTH)
                mesh = Mesh(edge_geo, edge_mat)
                mesh.transform.translate(dx, dy, 0)

                self.scene.add(mesh)
