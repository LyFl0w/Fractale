#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import os
import queue
from os.path import exists

import pygame.display

from program.utils import path


class QueueUpdate:

    def __init__(self, app):
        self.app = app
        self.__queue = queue.Queue()

    def execute(self):
        if not self.__queue.empty():
            key = self.__queue.get()

            if key == "screen_size":
                from program.settings.settingsbase import screen_settings
                self.app.screen = pygame.display.set_mode(screen_settings.get_native_size())
                self.__update_fractal()

            elif key == "fractal":
                self.app.fractal_manager.update_fractal_type()
                self.__update_fractal()

            elif key == "update_fractal":
                self.__update_fractal()

            elif key == "screenshot":
                screenshot_path = path.SCREENSHOT_PATH
                if not exists(screenshot_path):
                    os.mkdir(screenshot_path)
                files = next(os.walk(screenshot_path))[2]
                pygame.image.save(self.app.screen, os.path.join(screenshot_path, "screeshot_"+str(len(files))+".jpg"))

    def __update_fractal(self):
        self.app.draw_fractal()
        pygame.display.update()

    def put(self, key):
        self.__queue.put(key)
