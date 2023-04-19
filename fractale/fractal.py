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
    MANDELBROT = "Mandelbrot", 1
    JULIA = "Julia", 1
    SPONGE_CUBE = "Sponge Cube", 5
    SIERPINSKY = "Triangle de Sierpiński", 5
