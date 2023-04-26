#
#  Fracteur Copyright (c) 2023 LyFlow
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#

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
