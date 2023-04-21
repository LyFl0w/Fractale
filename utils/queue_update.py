import os
import queue
from os.path import exists

import pygame.display

from utils import path


class QueueUpdate:

    def __init__(self, app):
        self.app = app
        self.__queue = queue.Queue()

    def execute(self):
        if not self.__queue.empty():
            key, value = self.__queue.get()

            if key == "screen_size":
                from settings.settings import screen_settings
                self.app.screen = pygame.display.set_mode(screen_settings.get_native_size())
                self.app.draw_fractal()
                pygame.display.update()

            elif key == "downsampling":
                self.app.draw_fractal()
                pygame.display.update()

            elif key == "fractal":
                self.app.fractal_manager.update_fractal_type()
                self.app.draw_fractal()
                pygame.display.update()

            elif key == "screenshot":
                screenshot_path = path.DATA_SCREENSHOT_PATH
                if not exists(screenshot_path):
                    os.mkdir(screenshot_path)
                files = next(os.walk(screenshot_path))[2]
                pygame.image.save(self.app.screen, os.path.join(screenshot_path, "screeshot_"+str(len(files))+".jpg"))

    def put(self, key, value):
        self.__queue.put((key, value))
