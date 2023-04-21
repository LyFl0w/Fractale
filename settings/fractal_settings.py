import fractal.fractal
from settings import settings
from settings.settings import Settings


class FractalSettings(Settings):

    def __init__(self):
        self.fractal_type = fractal.fractal.FractalType.MANDELBROT.name
        self.iteration = 10
        self.fractal_power = 2

        super().__init__("fractal")

        settings.fractal_settings = self
