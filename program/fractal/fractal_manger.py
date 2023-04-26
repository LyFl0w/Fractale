#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import pygame

from program import interface
from program.fractal import fractalbase
from program.fractal.fractal_type.julia import Julia
from program.fractal.fractal_type.mandelbrot import Mandelbrot
from program.fractal.fractal_type.sierpinski import Sierpinski
from program.fractal.fractal_type.sponge_cube import SpongeCube
from program.fractal.fractalbase import FractalType


class FractalManager:

    def __init__(self, zoom: float):
        from program.settings.settingsbase import fractal_settings

        # center[0] -> x / center [1] -> y
        self.center = [0, 0]

        self.default_zoom = zoom
        self.zoom = zoom

        self.__fractal = None
        self.__fractal_type = fractalbase.get_fractal_by_name(fractal_settings.fractal_type)
        self.__update_fractal()

    def __update_fractal(self):
        from program.settings.settingsbase import fractal_settings

        self.center = [0, 0]
        self.zoom = self.default_zoom

        fractal_settings.iteration = max(min(fractal_settings.iteration, self.__fractal_type.iteration_max), self.__fractal_type.iteration_min)
        interface.update_iteration(self.__fractal_type)

        if self.__fractal_type == FractalType.MANDELBROT:
            self.__fractal = Mandelbrot(self)
        elif self.__fractal_type == FractalType.JULIA:
            self.__fractal = Julia(self)
        elif self.__fractal_type == FractalType.SPONGE_CUBE:
            self.__fractal = SpongeCube(self)
        elif self.__fractal_type == FractalType.SIERPINSKI:
            self.__fractal = Sierpinski(self)

    def get_fractal_type(self):
        return self.__fractal_type

    def update_fractal_type(self):
        from program.settings.settingsbase import fractal_settings

        self.__fractal_type = fractalbase.get_fractal_by_name(fractal_settings.fractal_type)
        self.__update_fractal()

    def draw(self, screen):
        from program.settings.settingsbase import screen_settings

        fractal_surface = self.__fractal.get_surface()

        if screen_settings.get_generation_size_optimization() != 1:
            fractal_surface = pygame.transform.scale(fractal_surface, screen_settings.get_native_size())

        screen.blit(fractal_surface, (0, 0))

        if screen_settings.display_filter:
            screen.fill(screen_settings.filter, special_flags=8)
