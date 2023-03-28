import numpy as np
import pygame
from pygame.surface import Surface

from fractale.fractal import Fractal


class Mandelbrot(Fractal):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.fractal_value = None

    def get_surface(self) -> Surface:
        diverge = np.zeros((self.fractal_manager.size[1], self.fractal_manager.size[0]), dtype=bool)
        divtime = np.full((self.fractal_manager.size[1], self.fractal_manager.size[0]), self.fractal_manager.iteration,
                          dtype=int)

        xmin, xmax = self.fractal_manager.center[0] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            0] + 1 / self.fractal_manager.zoom
        ymin, ymax = self.fractal_manager.center[1] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            1] + 1 / self.fractal_manager.zoom
        X, Y = np.meshgrid(np.linspace(xmin, xmax, self.fractal_manager.size[0]),
                           np.linspace(ymin, ymax, self.fractal_manager.size[1]))
        z = X + Y * 1j
        fractal = z if self.fractal_value is None else self.fractal_value

        for i in range(self.fractal_manager.iteration):
            z = z ** self.fractal_manager.fractal_power + fractal
            diverge = np.logical_or(diverge, z * np.conj(z) > 2 ** 2)
            divtime[np.logical_and(diverge, divtime == self.fractal_manager.iteration)] = i
            z[diverge] = 2

        fractal_array = np.flipud(np.rot90(divtime))
        fractal_surface = pygame.surfarray.make_surface(fractal_array)
        pygame.surfarray.blit_array(fractal_surface, fractal_array)
        return fractal_surface
