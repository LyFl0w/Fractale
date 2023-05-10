#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#


from abc import abstractmethod, ABC
from enum import Enum

from pygame import Surface


# Class abstraite permettant de créer les Fractales
class FractalBase(ABC):

    # Initialisation des Class fille (obligation de la variable Fractal Manager permettant de récupérer des informations important pour la Fractale)
    def __init__(self, fractal_manager):
        self.fractal_manager = fractal_manager

    # Fonction abstraite permettant de récupérer la Surface PyGame de la Fractale
    @abstractmethod
    def get_surface(self) -> Surface:
        pass


# Enumération des Fractales avec leurs paramètres par défaut
class FractalType(Enum):

    # Exemple : MANDELBROT -> nom : "Mandelbrot", sensibilité par défaut : 1, itération minimum : 6, itération maximum : 200
    MANDELBROT = ("Mandelbrot", 1, 6, 200)
    JULIA = ("Julia", 1, 6, 200)
    SPONGE_CUBE = ("Sponge Cube", 150, 4, 5)
    SIERPINSKI = ("Triangle de Sierpiński", 150, 3, 8)

    # Initialisation des variables d'énumération
    def __init__(self, real_name: str, default_sensibility: int, iteration_min: int, iteration_max: int):
        self.real_name = real_name
        self.default_sensibility = default_sensibility
        self.iteration_min = iteration_min
        self.iteration_max = iteration_max


# Fonction de référence permettant de récupérer l'énumération associé au vrai nom de la Fractal (Exemple : "Sponge Cube" -> SPONGE_CUBE)
def get_fractal_type_by_real_name(real_name: str) -> FractalType:
    for fractals in FractalType:
        if fractals.real_name == real_name:
            return fractals
    raise Exception(real_name, "fractal doesn't exist")


# Fonction de référence permettant de récupérer l'énumération associé au nom de son énumération de  la Fractal (Exemple : "SPONGE_CUBE" -> SPONGE_CUBE)
def get_fractal_by_name(name: str) -> FractalType:
    for fractals in FractalType:
        if fractals.name == name:
            return fractals
    raise Exception(name, "fractal doesn't exist")
