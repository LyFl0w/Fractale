#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


from program.fractal.fractal_type.mandelbrot import Mandelbrot


class Julia(Mandelbrot):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.fractal_value = -0.835 - 0.2321j
