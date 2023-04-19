from settings import settings
from settings.settings import Settings


class ScreenSettings(Settings):

    def __init__(self):
        print("load")
        self.native_size = [800, 800]
        self.scale_size = [800, 800]
        self.filter = (255, 255, 255)
        self.fps = 60

        self.draw_cursor = False

        super().__init__("screen")

        settings.screen_settings = self
        print("end load")
