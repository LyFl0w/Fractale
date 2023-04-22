import numpy as np
import pygame
from pygame.surface import Surface

from program.fractal.fractalbase import FractalBase


class Mandelbrot(FractalBase):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.fractal_value = None

    def get_surface(self) -> Surface:
        from program.settings.settingsbase import screen_settings, fractal_settings
        diverge = np.zeros((screen_settings.get_generation_size()[1], screen_settings.get_generation_size()[0]), dtype=bool)
        divtime = np.full((screen_settings.get_generation_size()[1], screen_settings.get_generation_size()[0]), fractal_settings.iteration,
                          dtype=int)

        xmin, xmax = self.fractal_manager.center[0] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            0] + 1 / self.fractal_manager.zoom
        ymin, ymax = self.fractal_manager.center[1] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            1] + 1 / self.fractal_manager.zoom
        X, Y = np.meshgrid(np.linspace(xmin, xmax, screen_settings.get_generation_size()[0]),
                           np.linspace(ymin, ymax, screen_settings.get_generation_size()[1]))
        z = X + Y * 1j
        fractal = z if self.fractal_value is None else self.fractal_value

        for i in range(fractal_settings.iteration):
            z = z ** fractal_settings.fractal_power + fractal
            diverge = np.logical_or(diverge, z * np.conj(z) > 2 ** 2)
            divtime[np.logical_and(diverge, divtime == fractal_settings.iteration)] = i
            z[diverge] = 2

        fractal_array = np.flipud(np.rot90(divtime))
        fractal_surface = pygame.surfarray.make_surface(fractal_array)
        pygame.surfarray.blit_array(fractal_surface, fractal_array)
        return fractal_surface
