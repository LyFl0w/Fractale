# ABSTRACT CLASS TO MAKE FRACTAL CLASS
from abc import abstractmethod, ABC
from enum import Enum

from pygame import Surface


class Fractal(ABC):
    def __init__(self, fractal_manager):
        self.fractal_manager = fractal_manager

    @abstractmethod
    def get_surface(self) -> Surface:
        pass


class FractalType(Enum):

    # 1. Str name
    # 2. Default Sensibility Power
    # 3. iteration min
    # 4. iteration max

    MANDELBROT = "Mandelbrot", 1, 6, 200
    JULIA = "Julia", 1, 6, 200
    SPONGE_CUBE = "Sponge Cube", 150, 5, 5
    SIERPINSKY = "Triangle de Sierpiński", 150, 3, 8

