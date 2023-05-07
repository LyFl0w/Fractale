#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#
import numpy as np
import pygame
from numba import jit
from pygame import Surface

from program.fractal.fractalbase import FractalBase


@jit(nopython=True)
def julia(cx, cy, zx, zy, maxiter):
    for n in range(maxiter):
        zx2, zy2 = zx * zx, zy * zy
        if zx2 + zy2 > 4.0:
            return n
        zx, zy = zx2 - zy2 + cx, 2.0 * zx * zy + cy
    return 0


@jit(nopython=True)
def julia_set(xmin, xmax, ymin, ymax, width, height, maxiter, cx=0.3, cy=0.5):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            n3[i, j] = julia(cx, cy, r1[i], r2[j], maxiter)
    return n3


class Julia(FractalBase):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)

    def get_surface(self) -> Surface:
        from program.settings.settingsbase import fractal_settings

        xmin, xmax = self.fractal_manager.center[0] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            0] + 1 / self.fractal_manager.zoom

        ymin, ymax = self.fractal_manager.center[1] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            1] + 1 / self.fractal_manager.zoom

        screen_width, screen_height = self.fractal_manager.get_fractal_details()
        maxiter = fractal_settings.iteration

        n3 = julia_set(xmin, xmax, ymin, ymax, screen_width, screen_height, maxiter)
        fractal_surface = pygame.surfarray.make_surface(n3)

        return fractal_surface
