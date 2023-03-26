import pygame

from fractale.fractal import FractalType
from fractale.fractal_type.julia import Julia
from fractale.fractal_type.mandelbrot import Mandelbrot


class FractalManager:

    def __init__(self, fractal_type: FractalType, size: tuple[int, int], center: tuple[int, int], zoom: float, iteration: int, fractal_power: int):
        self.fractal = None
        self.update_fractal_type(fractal_type)
        self.size = size
        self.center = center
        self.zoom = zoom
        self.iteration = iteration
        self.fractal_power = fractal_power

    def update_fractal_type(self, fractal_type):
        if fractal_type == FractalType.MANDELBROT:
            self.fractal = Mandelbrot(self)
        elif fractal_type == FractalType.JULIA:
            self.fractal = Julia(self)
        elif fractal_type == FractalType.SPONGE_CUBE:
            # self.fractal = SpongeCube(self)
            pass

    def draw(self, screen, native_size: tuple[int, int], color_filter=None):
        fractal_array = self.fractal.get_array()
        fractal_surface = pygame.surfarray.make_surface(fractal_array)
        pygame.surfarray.blit_array(fractal_surface, fractal_array)
        screen.blit(pygame.transform.scale(fractal_surface, native_size), (0, 0))

        if color_filter is not None:
            screen.fill(pygame.color.Color(color_filter), special_flags=8)
