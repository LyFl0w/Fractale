import pygame
from pygame import Surface

from fractal.fractal import Fractal


class Sierpinsky(Fractal):

    def __init__(self, fractal_manager):
        from settings.settings import screen_settings

        super().__init__(fractal_manager)
        self.fractal_value = None
        self.diff = [screen_settings.get_generation_size()[1] / 2, screen_settings.get_generation_size()[0] / 2]
        self.triangle = pygame.Surface(screen_settings.get_generation_size(), pygame.SRCALPHA)
        pygame.draw.polygon(self.triangle, (255, 255, 255),
                            ([0, 0],
                             [screen_settings.get_generation_size()[1] // 2, screen_settings.get_generation_size()[0]],
                             [screen_settings.get_generation_size()[1], 0]), 0)

        self.fractal_manager.center = [0, -400]

    def fractale_matrice_triangle(self, screen, zoom=1.0, maxit=1, taille=1.0, x=0.0, y=0.0, distance=False):
        if maxit > 0:
            screen.blit(pygame.transform.scale(self.triangle, (int(taille * zoom), int(taille * zoom))),
                        (x * zoom + self.diff[0], y * zoom + self.diff[1]))
            self.fractale_matrice_triangle(screen, zoom, maxit - 1, taille / 2, x - taille / 4, y + taille / 2,
                                           distance)
            self.fractale_matrice_triangle(screen, zoom, maxit - 1, taille / 2, x + taille * 0.75, y + taille / 2,
                                           distance)
            self.fractale_matrice_triangle(screen, zoom, maxit - 1, taille / 2, x + taille / 4, y - taille * 0.5,
                                           distance)

    def get_surface(self) -> Surface:
        from settings.settings import screen_settings, fractal_settings

        mb = pygame.Surface(screen_settings.get_generation_size())
        mb.fill((0, 0, 0))

        h_triangle = screen_settings.get_generation_size()[1]
        w_triangle = screen_settings.get_generation_size()[0] * 2
        point_gauche = [self.diff[0] + self.fractal_manager.center[0] - w_triangle,
                        self.diff[1] + self.fractal_manager.center[1] + h_triangle]
        point_droit = [self.diff[0] + self.fractal_manager.center[0] + w_triangle,
                       self.diff[1] + self.fractal_manager.center[1] + h_triangle]
        point_haut = [self.diff[0] + self.fractal_manager.center[0],
                      self.diff[1] + self.fractal_manager.center[1] - h_triangle]

        pygame.draw.polygon(mb, (0, 0, 0), (point_gauche, point_droit, point_haut), 0)

        taille = screen_settings.get_generation_size()[1]
        x = (point_haut[0] + point_gauche[0]) / 2
        y = (point_haut[1] + point_gauche[1]) / 2

        self.fractale_matrice_triangle(mb, zoom=self.fractal_manager.zoom, maxit=2,
                                       taille=taille, x=x, y=y)

        return pygame.transform.flip(mb, True, False)
