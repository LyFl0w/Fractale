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


# Class gérant les Fractales pour PyGame
class FractalManager:

    def __init__(self, zoom: float):
        from program.settings.settingsbase import fractal_settings

        # Coordonné X et Y de la Fractale
        # center[0] -> x / center [1] -> y
        self.center = [0, 0]

        # Initialisation de la variable de la taille de la Fractale permettant de baisser la qualité lors des déplacement de la Fractale
        self.__fractal_details = None
        # Chargement de la variable __fractal_details pour l'associer aux bonnes valeurs
        self.update_downsampling()

        # Initialisation du zoom (soit de la coordonnée Z)
        self.default_zoom = zoom
        self.zoom = zoom

        # Initialisation de la variable stockant la Fractale
        self.__fractal = None
        # Variable ciblant le type de la Fractale en énumération
        self.__fractal_type = fractalbase.get_fractal_by_name(fractal_settings.fractal_type)
        # Chargement de la variable __fractal pour charger la Fractale en fonction du type de Fractale stocké par la variable __fractal_type
        self.__update_fractal()

    # Fonction mettant à jour la Fractale en fonction du type de Fractale stocké par la variable __fractal_type
    def __update_fractal(self):
        from program.settings.settingsbase import fractal_settings

        # Remet les coordonnées de la Fractale à 0 en X et Y ainsi que le zoom (donc la coordonnée Z)
        self.center = [0, 0]
        self.zoom = self.default_zoom

        # Met la bonne itération pour la Fractale
        fractal_settings.iteration = max(min(fractal_settings.iteration, self.__fractal_type.iteration_max),
                                         self.__fractal_type.iteration_min)
        # Met à jour l'interface TKinter pour avoir la bonne itération
        interface.update_iteration(self.__fractal_type)

        # Génére la bonne Fractale en fonction du type de la Fractale
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

    # Fonction permettant de changer de Fractale
    def update_fractal_type(self):
        from program.settings.settingsbase import fractal_settings

        self.__fractal_type = fractalbase.get_fractal_by_name(fractal_settings.fractal_type)
        self.__update_fractal()

    def get_fractal(self):
        return self.__fractal

    # Fonction permettant d'afficher la Fractale sur l'écran PyGame
    def draw(self, screen):
        from program.settings.settingsbase import screen_settings

        # Récupère la Surface de la Fractale
        fractal_surface = self.__fractal.get_surface().convert()

        # Met de l'antialiasing si la qualité de la Fractale est suppérieur à 100%
        if screen_settings.get_generation_size_optimization() > 1:
            # Met la Fractale généré dans la taille de l'écran (avec l'antialiasing)
            fractal_surface = pygame.transform.smoothscale(fractal_surface, screen_settings.get_native_size())
        else:
            # Met la Fractale généré dans la taille de l'écran (sans l'antialiasing)
            fractal_surface = pygame.transform.scale(fractal_surface, screen_settings.get_native_size())

        # Affiche la fractale sur l'écran PyGame
        screen.blit(fractal_surface, (0, 0))

        # Affiche le filtre si il y'en a un
        if screen_settings.display_filter:
            screen.fill(screen_settings.filter, special_flags=8)

    # Fonction mettant à jour la qualité de la Fractale lors des déplacements de l'utilisateur
    def update_downsampling(self, details=1.0):
        from program.settings.settingsbase import screen_settings

        self.__fractal_details = [int(screen_settings.get_generation_size()[0] * details),
                                  int(screen_settings.get_generation_size()[1] * details)]

    # Fonction permettant de récupérer la taille dans laquelle la Fractale doit être généré
    def get_fractal_details(self):
        return self.__fractal_details
