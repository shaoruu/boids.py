import math
import numpy as np


class OrbitControl(object):
    def __init__(self, object):
        self.object = object

        self.enabled = True

        self.target = np.array([0, 0, 0])

        self.min_distance = 0
        self.max_distance = math.inf

        self.min_zoom = 0
        self.max_zoom = math.inf

        self.min_polar_angle = 0
        self.max_polar_angle = math.pi

        self.min_azimuth_angle = -math.inf
        self.max_azimuth_angle = math.inf

        self.enable_damping = False
        self.damping_factor = 0.1

        self.enable_zoom = True
        self.zoom_speed = 1.0

        self.enable_rotate = True
        self.rotate_speed = 0.1

        self.enable_pan = True
        self.pan_speed = 0.1
        self.screen_space_panning = False
        self.key_pan_speed = 7.0

        self.auto_rotate = False
        self.auto_rotate_speed = 2.0

        self.enable_keys = True

        self.target0 = np.copy(self.target)
        self.position0 = self.object.transform.getPosition()
        # self.zoom0 = self.object.zoom

    # def get_polar_angle(self)
