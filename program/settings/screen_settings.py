#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


from program.settings import settingsbase
from program.settings.settingsbase import Settings


# Class de paramètre associé directement au paramètre de l'écran
class ScreenSettings(Settings):

    def __init__(self):
        # Taille native de l'écran
        self.__native_size = (800, 800)
        # Facteur d'optimisation (0.9 -> 90% de la taille de l'écran pour généré la Fractale, permettant des calculs plus rapide)
        self.__generation_size_optimization = 0.9
        # Taille permettant de calculer les Fractales
        self.__generation_size = (int(self.__native_size[0] * self.__generation_size_optimization),
                                  int(self.__native_size[1] * self.__generation_size_optimization))

        # Sensibilité de la souris
        self.sensibility = 5
        # Couleur du Filtre
        self.filter = (255, 255, 150)
        # Fps maximum
        self.fps = 60

        # Affichage du curseur
        self.display_cursor = True
        # Affichage du filtre
        self.display_filter = False

        # Création / Chargement du fichier de paramètre d'écran
        super().__init__("screen")

        # Permet un accès statique pour être récupéré facilement partout depuis le fichier settingsbase.py
        settingsbase.screen_settings = self

    def get_native_size(self):
        return self.__native_size

    def set_native_size(self, native_size: tuple[int, int]):
        self.__native_size = native_size
        self.set_generation_size_optimization(self.__generation_size_optimization)

    def get_generation_size_optimization(self):
        return self.__generation_size_optimization

    def set_generation_size_optimization(self, generation_size_optimization: float):
        self.__generation_size_optimization = generation_size_optimization
        self.__generation_size = (int(self.__native_size[0] * self.__generation_size_optimization),
                                  int(self.__native_size[1] * self.__generation_size_optimization))
        self.save()

    def get_generation_size(self) -> tuple[int, int]:
        return self.__generation_size
