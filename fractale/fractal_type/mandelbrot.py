import numpy as np
from numpy import ndarray
from fractale.fractal import Fractal


class Mandelbrot(Fractal):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.fractal_value = None

    def get_array(self) -> ndarray:
        diverge = np.zeros((self.fractal_manager.size[1], self.fractal_manager.size[0]), dtype=bool)
        divtime = np.full((self.fractal_manager.size[1], self.fractal_manager.size[0]), self.fractal_manager.iteration,
                          dtype=int)

        xmin, xmax = self.fractal_manager.center[0] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            0] + 1 / self.fractal_manager.zoom
        ymin, ymax = self.fractal_manager.center[1] - 1 / self.fractal_manager.zoom, self.fractal_manager.center[
            1] + 1 / self.fractal_manager.zoom
        X, Y = np.meshgrid(np.linspace(xmin, xmax, self.fractal_manager.size[0]),
                           np.linspace(ymin, ymax, self.fractal_manager.size[1]))
        z = X + Y * 1j
        fractal = z if self.fractal_value is None else self.fractal_value

        for i in range(self.fractal_manager.iteration):
            z = z ** self.fractal_manager.fractal_power + fractal
            diverge = np.logical_or(diverge, z * np.conj(z) > 2 ** 2)
            divtime[np.logical_and(diverge, divtime == self.fractal_manager.iteration)] = i
            z[diverge] = 2

        return np.flipud(np.rot90(divtime))
