#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import os
import queue
from os.path import exists

import pygame.display

from program.fractal.fractalbase import FractalType
from program.utils import path


class QueueUpdate:

    def __init__(self, app):
        self.app = app
        self.__queue = queue.Queue()

    def execute(self):
        if not self.__queue.empty():
            key = self.__queue.get()

            # Change la taille de l'écran PyGame
            if key == "screen_size":
                from program.settings.settingsbase import screen_settings
                self.app.screen = pygame.display.set_mode(screen_settings.get_native_size())

                self.__update_fractal_init_properties()
                self.app.fractal_manager.update_downsampling()
                self.__update_fractal()

            # Change la qualité de la Fractale
            elif key == "downsampling":
                self.__update_fractal_init_properties()
                self.app.fractal_manager.update_downsampling()
                self.__update_fractal()

            # Met à jour le type de Fractale
            elif key == "fractal":
                self.app.fractal_manager.update_fractal_type()
                self.__update_fractal()

            # Met à jour le rendu de la Fractale
            elif key == "update_fractal":
                self.__update_fractal()

            # Prend une captrue d'écran de la Fractale
            elif key == "screenshot":
                screenshot_path = path.SCREENSHOT_PATH
                if not exists(screenshot_path):
                    os.mkdir(screenshot_path)
                files = next(os.walk(screenshot_path))[2]
                pygame.image.save(self.app.screen, os.path.join(screenshot_path, "screeshot_"+str(len(files))+".jpg"))

    # Fonction de référence
    def __update_fractal(self):
        self.app.draw_fractal()
        pygame.display.update()

    # Met à jour les propriété de certaine initialisé lors de leur chargement (taille de motif, etc...)
    def __update_fractal_init_properties(self):
        if self.app.fractal_manager.get_fractal_type() in [FractalType.SIERPINSKI, FractalType.SPONGE_CUBE]:
            self.app.fractal_manager.get_fractal().update()

    def put(self, key):
        self.__queue.put(key)
