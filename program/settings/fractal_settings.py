#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


from program.fractal import fractalbase
from program.settings import settingsbase
from program.settings.settingsbase import Settings


# Class de paramètre associé directement au Fractale
class FractalSettings(Settings):

    def __init__(self):
        # Nom de la Fractale par défaut
        self.fractal_type = fractalbase.FractalType.MANDELBROT.name
        # Itération de la Fractale par défaut
        self.iteration = 10
        # Puissance pour la Fractale Mandelbrot par défaut
        self.fractal_power = 2
        # Valeur de la Fractale Julia par défaut
        self.c = [-0.8, 0.156]

        # Création / Chargement du fichier de paramètre de la Fractale
        super().__init__("fractal")

        # Permet un accès statique pour être récupéré facilement partout depuis le fichier settingsbase.py
        settingsbase.fractal_settings = self
