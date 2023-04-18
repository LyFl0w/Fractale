import pygame
from fractale.fractal import FractalType
from fractale.fractal_type.julia import Julia
from fractale.fractal_type.mandelbrot import Mandelbrot
from fractale.fractal_type.sierpinsky import Sierpinsky
from fractale.fractal_type.sponge_cube import SpongeCube


class FractalManager:

    def __init__(self, fractal_type: FractalType, size: list[int, int], center: list[int, int], zoom: float,
                 iteration: int, fractal_power: int):
        # size[0] -> width / size [1] -> height
        self.size = size
        # center[0] -> x / center [1] -> y
        self.center = center

        self.zoom = zoom
        self.iteration = iteration
        self.fractal_power = fractal_power

        self.fractal = None
        self.update_fractal_type(fractal_type)

    def update_fractal_type(self, fractal_type):
        if fractal_type == FractalType.MANDELBROT:
            self.fractal = Mandelbrot(self)
        elif fractal_type == FractalType.JULIA:
            self.fractal = Julia(self)
        elif fractal_type == FractalType.SPONGE_CUBE:
            self.fractal = SpongeCube(self)
        elif fractal_type == FractalType.SIERPINSKY:
            self.fractal = Sierpinsky(self)

    def draw(self, screen, native_size: tuple[int, int], color_filter=None):
        fractal_surface = self.fractal.get_surface()
        screen.blit(pygame.transform.scale(fractal_surface, native_size), (0, 0))

        if color_filter is not None:
            screen.fill(color_filter, special_flags=8)
