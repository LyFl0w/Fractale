import pygame

import fractal
from fractal.fractal import FractalType
from fractal.fractal_type.julia import Julia
from fractal.fractal_type.mandelbrot import Mandelbrot
from fractal.fractal_type.sierpinsky import Sierpinsky
from fractal.fractal_type.sponge_cube import SpongeCube


class FractalManager:

    def __init__(self, zoom: float):
        from settings.settings import fractal_settings

        # center[0] -> x / center [1] -> y
        self.center = [0, 0]

        self.zoom = zoom

        self.__fractal = None
        self.__fractal_type = fractal.fractal.get_fractal_by_name(fractal_settings.fractal_type)
        self.set_fractal_type(self.__fractal_type)

    def set_fractal_type(self, fractal_type: FractalType):
        self.center = [0, 0]
        self.__fractal_type = fractal_type
        if fractal_type == FractalType.MANDELBROT:
            self.__fractal = Mandelbrot(self)
        elif fractal_type == FractalType.JULIA:
            self.__fractal = Julia(self)
        elif fractal_type == FractalType.SPONGE_CUBE:
            self.__fractal = SpongeCube(self)
        elif fractal_type == FractalType.SIERPINSKY:
            self.__fractal = Sierpinsky(self)

    def get_fractal_type(self):
        return self.__fractal_type

    def draw(self, screen):
        from settings.settings import screen_settings

        fractal_surface = self.__fractal.get_surface()

        if screen_settings.get_generation_size_optimization() != 1:
            fractal_surface = pygame.transform.scale(fractal_surface, screen_settings.get_native_size())

        screen.blit(fractal_surface, (0, 0))

        if screen_settings.display_filter:
            screen.fill(screen_settings.filter, special_flags=8)
