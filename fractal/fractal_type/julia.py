from fractal.fractal_type.mandelbrot import Mandelbrot


class Julia(Mandelbrot):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.fractal_value = -0.835 - 0.2321j
