#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import math

import pygame
from numba import jit, njit
from pygame.surface import Surface

from program.fractal.fractalbase import FractalBase


@njit(fastmath=True, cache=True)
def position_cube(center_x, center_y, cube_x, cube_y, width):
    if center_x - cube_x >= width / 2:
        x = 1
    elif center_x - cube_x <= -width / 2:
        x = -1
    else:
        x = 0
    if center_y - cube_y >= width:
        y = 1
    elif center_y - cube_y <= -width:
        y = -1
    else:
        y = 0
    return [x, y]


class SpongeCube(FractalBase):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.diff = None
        self.update()

    def infini(self):
        from program.settings.settingsbase import screen_settings
        center_x, center_y = self.fractal_manager.center[0], self.fractal_manager.center[1]
        pos_cube = position_cube(center_x, center_y, 0, 0, screen_settings.get_generation_size()[1] / 3)
        bloc = position_cube(center_x, center_y, pos_cube[0] * screen_settings.get_generation_size()[1] / 3,
                             pos_cube[1] * screen_settings.get_generation_size()[1] / 3,
                             screen_settings.get_generation_size()[1] / 9)

        if self.fractal_manager.zoom >= 9:
            self.fractal_manager.zoom /= 3
            self.fractal_manager.center[0] = (screen_settings.get_generation_size()[1] / 3) * bloc[0] + (
                    self.fractal_manager.center[0] - (
                    pos_cube[0] * (screen_settings.get_generation_size()[0] / 3) + bloc[0] * (
                    screen_settings.get_generation_size()[0] / 9))) * 3
            self.fractal_manager.center[1] = (screen_settings.get_generation_size()[1] / 3) * bloc[1] + (
                    self.fractal_manager.center[1] - (
                    pos_cube[1] * (screen_settings.get_generation_size()[1] / 3) + bloc[1] * (
                    screen_settings.get_generation_size()[1] / 9))) * 3
        if abs(self.fractal_manager.center[0]) > self.diff[0]:
            if self.fractal_manager.center[0] > 0:
                self.fractal_manager.center[0] -= screen_settings.get_generation_size()[0]
            else:
                self.fractal_manager.center[0] += screen_settings.get_generation_size()[0]
        if abs(self.fractal_manager.center[1]) > self.diff[1]:
            if self.fractal_manager.center[1] > 0:
                self.fractal_manager.center[1] -= screen_settings.get_generation_size()[1]
            else:
                self.fractal_manager.center[1] += screen_settings.get_generation_size()[1]

        return [self.fractal_manager.center[0], self.fractal_manager.center[1]]

    def fractale_matrice(self, zoom, screen, h_carre, w_carre, maxit, x=0, y=0, distance=False):
        from program.settings.settingsbase import screen_settings

        a = 0
        next_distance = False
        if distance:
            if math.sqrt(x ** 2 + y ** 2) <= screen_settings.get_generation_size()[0]:
                distance = False
                next_distance = True
        if maxit > 0:
            if not distance:
                a += 1
                pygame.draw.rect(screen, (255, 255, 255), (
                    ((x - (w_carre / 3 / 2)) * zoom + self.diff[0]), ((y - (h_carre / 3 / 2)) * zoom + self.diff[1]),
                    int((w_carre / 3) * zoom), int((h_carre / 3) * zoom)), 0)
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (i, j) != (0, 0):
                            a += self.fractale_matrice(zoom, screen, h_carre / 3, w_carre / 3, maxit - 1,
                                                       x + (w_carre / 3) * i,
                                                       y + (h_carre / 3) * j, next_distance)
        return a

    def get_surface(self) -> Surface:
        from program.settings.settingsbase import screen_settings, fractal_settings

        mb = pygame.Surface(screen_settings.get_generation_size())
        self.fractal_manager.center = self.infini()
        self.fractale_matrice(zoom=self.fractal_manager.zoom, screen=mb,
                              h_carre=screen_settings.get_generation_size()[1],
                              w_carre=screen_settings.get_generation_size()[0], maxit=fractal_settings.iteration,
                              x=-self.fractal_manager.center[0], y=self.fractal_manager.center[1])

        for i in range(-1, 2):
            for y in range(-1, 2):
                self.fractale_matrice(zoom=self.fractal_manager.zoom, screen=mb,
                                      h_carre=screen_settings.get_generation_size()[1],
                                      w_carre=screen_settings.get_generation_size()[0],
                                      maxit=fractal_settings.iteration,
                                      x=-self.fractal_manager.center[0] + i * screen_settings.get_generation_size()[0],
                                      y=self.fractal_manager.center[1] + y * screen_settings.get_generation_size()[1],
                                      distance=True)

        return pygame.transform.flip(mb, False, True)

    def update(self):
        from program.settings.settingsbase import screen_settings
        self.diff = [screen_settings.get_generation_size()[0] / 2, screen_settings.get_generation_size()[1] / 2]
