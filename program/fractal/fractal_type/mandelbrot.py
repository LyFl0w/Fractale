#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#
import numba
from numba import jit, njit
import numpy as np
import pygame
from pygame.surface import Surface
from program.fractal.fractalbase import FractalBase


@njit(fastmath=True, cache=True)
def __mandelbrot(c, maxiter, power):
    z = c
    for n in range(maxiter):
        if z.real * z.real + z.imag * z.imag > 4.0:
            return n
        z = z ** power + c
    return 0


@njit(fastmath=True, parallel=True, cache=True)
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter, power):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in numba.prange(width):
        for j in numba.prange(height):
            n3[i, j] = __mandelbrot(r1[i] + 1j * r2[j], maxiter, power)
    return n3


class Mandelbrot(FractalBase):

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

        n3 = mandelbrot_set(xmin, xmax, ymin, ymax, screen_width, screen_height, maxiter,
                            fractal_settings.fractal_power)
        fractal_surface = pygame.surfarray.make_surface(n3)

        return fractal_surface
