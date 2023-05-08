#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import pygame
from pygame import Surface

from program.fractal.fractalbase import FractalBase


class Sierpinski(FractalBase):

    def __init__(self, fractal_manager):
        super().__init__(fractal_manager)
        self.diff, self.triangle = None, None
        self.update()
        self.fractal_manager.center = [0, -400]

    def fractale_matrice_triangle(self, screen, zoom=1.0, maxit=1, largeur=1.0, hauteur=1.0, x=0.0, y=0.0,
                                  distance=False):
        if maxit > 0:
            n_it = maxit - 1
            n_largeur = largeur / 2
            n_hauteur = hauteur / 2
            screen.blit(pygame.transform.scale(self.triangle, (int(largeur * zoom), int(hauteur * zoom))),
                        (x * zoom + self.diff[0], y * zoom + self.diff[1]))
            self.fractale_matrice_triangle(screen, zoom, n_it, n_largeur, n_hauteur, x - largeur / 4,
                                           y + hauteur / 2,
                                           distance)
            self.fractale_matrice_triangle(screen, zoom, n_it, n_largeur, n_hauteur, x + largeur * 0.75,
                                           y + hauteur / 2,
                                           distance)
            self.fractale_matrice_triangle(screen, zoom, n_it, n_largeur, n_hauteur, x + largeur / 4,
                                           y - hauteur * 0.5,
                                           distance)

    def get_surface(self) -> Surface:
        from program.settings.settingsbase import screen_settings, fractal_settings

        mb = pygame.Surface(screen_settings.get_generation_size())
        mb.fill((0, 0, 0))

        h_triangle = screen_settings.get_generation_size()[1]
        w_triangle = screen_settings.get_generation_size()[0] * 2
        point_gauche = [self.diff[0] + self.fractal_manager.center[0] - w_triangle,
                        self.diff[1] + self.fractal_manager.center[1] + h_triangle]

        point_haut = [self.diff[0] + self.fractal_manager.center[0],
                      self.diff[1] + self.fractal_manager.center[1] - h_triangle]

        x = (point_haut[0] + point_gauche[0]) / 2
        y = (point_haut[1] + point_gauche[1]) / 2

        self.fractale_matrice_triangle(mb, zoom=self.fractal_manager.zoom, maxit=fractal_settings.iteration,
                                       largeur=w_triangle // 2, hauteur=h_triangle, x=x, y=y)

        return pygame.transform.flip(mb, True, False)

    def update(self):
        from program.settings.settingsbase import screen_settings
        self.diff = [screen_settings.get_generation_size()[0] / 2, screen_settings.get_generation_size()[1] / 2]
        self.triangle = pygame.Surface(screen_settings.get_generation_size(), pygame.SRCALPHA)
        pygame.draw.polygon(self.triangle, (255, 255, 255),
                            ([0, 0],
                             [screen_settings.get_generation_size()[0] // 2, screen_settings.get_generation_size()[1]],
                             [screen_settings.get_generation_size()[0], 0]), 0)
