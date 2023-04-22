from program.fractal import fractalbase
from program.settings import settingsbase
from program.settings.settingsbase import Settings


class FractalSettings(Settings):

    def __init__(self):
        self.fractal_type = fractalbase.FractalType.MANDELBROT.name
        self.iteration = 10
        self.fractal_power = 2

        super().__init__("fractal")

        settingsbase.fractal_settings = self
