import math

import pygame
from pygame.surface import Surface

from fractale.fractal import Fractal


class SpongeCube(Fractal):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.fractal_value = None
        self.diff = [self.fractal_manager.size[1] / 2, self.fractal_manager.size[0] / 2]

    def position_cube(self, cube_x, cube_y, width):
        if self.fractal_manager.center[0] - cube_x >= width / 2:
            x = 1
        elif self.fractal_manager.center[0] - cube_x <= -width / 2:
            x = -1
        else:
            x = 0
        if self.fractal_manager.center[1] - cube_y >= width:
            y = 1
        elif self.fractal_manager.center[1] - cube_y <= -width:
            y = -1
        else:
            y = 0
        return [x, y]

    def infini(self):
        pos_cube = self.position_cube(0, 0, self.fractal_manager.size[1] / 3)
        bloc = self.position_cube(pos_cube[0] * self.fractal_manager.size[1] / 3,
                                  pos_cube[1] * self.fractal_manager.size[1] / 3, self.fractal_manager.size[1] / 9)

        if self.fractal_manager.zoom >= 9:
            self.fractal_manager.zoom /= 3
            self.fractal_manager.center[0] = (self.fractal_manager.size[1] / 3) * bloc[0] + (
                    self.fractal_manager.center[0] - (pos_cube[0] * (self.fractal_manager.size[1] / 3) + bloc[0] * (
                        self.fractal_manager.size[1] / 9))) * 3
            self.fractal_manager.center[1] = (self.fractal_manager.size[1] / 3) * bloc[1] + (
                    self.fractal_manager.center[1] - (pos_cube[1] * (self.fractal_manager.size[1] / 3) + bloc[1] * (
                        self.fractal_manager.size[1] / 9))) * 3
        if abs(self.fractal_manager.center[0]) > self.diff[0]:
            if self.fractal_manager.center[0] > 0:
                self.fractal_manager.center[0] -= self.fractal_manager.size[0]
            else:
                self.fractal_manager.center[0] += self.fractal_manager.size[0]
        if abs(self.fractal_manager.center[1]) > self.diff[1]:
            if self.fractal_manager.center[1] > 0:
                self.fractal_manager.center[1] -= self.fractal_manager.size[1]
            else:
                self.fractal_manager.center[1] += self.fractal_manager.size[1]

        return [self.fractal_manager.center[0], self.fractal_manager.center[1]]

    def fractale_matrice(self, zoom, screen, h_carre, w_carre, maxit, x=0, y=0, distance=False):
        a = 0
        next_distance = False
        if distance:
            if math.sqrt(x ** 2 + y ** 2) <= self.fractal_manager.size[0]:
                distance = False
                next_distance = True
        if maxit > 0:
            if not distance:
                a += 1
                pygame.draw.rect(screen, (255, 255, 255), (
                    ((x - (h_carre / 3 / 2)) * zoom + self.diff[0]), ((y - (w_carre / 3 / 2)) * zoom + self.diff[1]),
                    int((w_carre / 3) * zoom), int((h_carre / 3) * zoom)), 0)
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (i, j) != (0, 0):
                            a += self.fractale_matrice(zoom, screen, h_carre / 3, w_carre / 3, maxit - 1, x + (w_carre / 3) * i,
                                                       y + (h_carre / 3) * j, next_distance)
        return a

    def get_surface(self) -> Surface:
        mb = pygame.Surface(self.fractal_manager.size)
        self.fractal_manager.center = self.infini()
        self.fractale_matrice(zoom=self.fractal_manager.zoom, screen=mb, h_carre=self.fractal_manager.size[1],
                              w_carre=self.fractal_manager.size[0], maxit=self.fractal_manager.iteration,
                              x=-self.fractal_manager.center[0], y=self.fractal_manager.center[1])

        for i in range(-1, 2):
            for y in range(-1, 2):
                self.fractale_matrice(zoom=self.fractal_manager.zoom, screen=mb, h_carre=self.fractal_manager.size[1],
                                      w_carre=self.fractal_manager.size[0], maxit=self.fractal_manager.iteration,
                                      x=-self.fractal_manager.center[0] + i * self.fractal_manager.size[1],
                                      y=self.fractal_manager.center[1] + y * self.fractal_manager.size[0], distance=True)

        return pygame.transform.flip(mb, False, True)
