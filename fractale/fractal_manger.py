import pygame
from fractale.fractal import FractalType
from fractale.fractal_type.julia import Julia
from fractale.fractal_type.mandelbrot import Mandelbrot
from fractale.fractal_type.sierpinsky import Sierpinsky
from fractale.fractal_type.sponge_cube import SpongeCube


class FractalManager:

    def __init__(self, fractal_type: FractalType, zoom: float):
        from settings.settings import screen_settings

        # size[0] -> width / size [1] -> height
        self.size = screen_settings.generation_size
        # center[0] -> x / center [1] -> y
        self.center = [0, 0]

        self.zoom = zoom
        self.iteration = screen_settings.iteration
        self.fractal_power = screen_settings.fractal_power

        self.fractal = None
        self.fractal_type = fractal_type
        self.update_fractal_type(fractal_type)

    def update_fractal_type(self, fractal_type):
        self.center = [0, 0]
        if fractal_type == FractalType.MANDELBROT:
            self.fractal = Mandelbrot(self)
        elif fractal_type == FractalType.JULIA:
            self.fractal = Julia(self)
        elif fractal_type == FractalType.SPONGE_CUBE:
            self.fractal = SpongeCube(self)
        elif fractal_type == FractalType.SIERPINSKY:
            self.fractal = Sierpinsky(self)

    def draw(self, screen, native_size: tuple[int, int]):
        from settings.settings import screen_settings

        fractal_surface = self.fractal.get_surface()
        screen.blit(pygame.transform.scale(fractal_surface, native_size), (0, 0))

        if screen_settings.display_filter:
            screen.fill(screen_settings.filter, special_flags=8)
