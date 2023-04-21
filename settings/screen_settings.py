from typing import List

from settings import settings
from settings.settings import Settings


class ScreenSettings(Settings):

    def __init__(self):
        self.__native_size = (800, 800)
        self.__generation_size_optimization = 0.9
        self.__generation_size = (int(self.__native_size[0] * self.__generation_size_optimization),
                                  int(self.__native_size[1] * self.__generation_size_optimization))

        self.sensibility = 5
        self.filter = (255, 255, 255)
        self.fps = 60

        self.display_cursor = True
        self.display_filter = False

        super().__init__("screen")

        settings.screen_settings = self

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
