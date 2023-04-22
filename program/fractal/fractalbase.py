# ABSTRACT CLASS TO MAKE FRACTAL CLASS
from abc import abstractmethod, ABC
from enum import Enum

from pygame import Surface


class FractalBase(ABC):
    def __init__(self, fractal_manager):
        self.fractal_manager = fractal_manager

    @abstractmethod
    def get_surface(self) -> Surface:
        pass


class FractalType(Enum):
    MANDELBROT = ("Mandelbrot", 1, 6, 200)
    JULIA = ("Julia", 1, 6, 200)
    SPONGE_CUBE = ("Sponge Cube", 150, 5, 5)
    SIERPINSKY = ("Triangle de Sierpiński", 150, 3, 8)

    def __init__(self, real_name: str, default_sensibility: int, iteration_min: int, iteration_max: int):
        self.real_name = real_name
        self.default_sensibility = default_sensibility
        self.iteration_min = iteration_min
        self.iteration_max = iteration_max


def get_fractal_type_by_real_name(real_name: str) -> FractalType:
    for fractals in FractalType:
        if fractals.real_name == real_name:
            return fractals
    raise Exception(real_name, "fractal doesn't exist")


def get_fractal_by_name(name: str) -> FractalType:
    for fractals in FractalType:
        if fractals.name == name:
            return fractals
    raise Exception(name, "fractal doesn't exist")
