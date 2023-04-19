from settings import settings
from settings.settings import Settings


class ScreenSettings(Settings):

    def __init__(self):
        self.native_size = [800, 800]
        self.generation_size = [800, 800]

        self.iteration = 10
        self.fractal_power = 2
        self.filter = (255, 255, 255)
        self.fps = 60

        self.display_cursor = True
        self.display_filter = False

        super().__init__("screen")

        settings.screen_settings = self
