import pygame

from fractal.fractal import FractalType
from fractal.fractal_manger import FractalManager
from settings.fractal_settings import FractalSettings
from settings.screen_settings import ScreenSettings


class App:
    def __init__(self):
        ScreenSettings()
        FractalSettings()

        self.fractal_manager = FractalManager(zoom=0.5)

        from settings.settings import screen_settings

        self.screen = pygame.display.set_mode(screen_settings.native_size)
        self.clock = pygame.time.Clock()

        self.running = False
        self.draw_cursor = False

    def zoom_at_cursor(self, zoom_factor):
        from settings.settings import screen_settings

        self.fractal_manager.zoom *= zoom_factor
        self.fractal_manager.draw(self.screen)
        if self.draw_cursor:
            pygame.draw.circle(self.screen,
                               screen_settings.filter[::-1] if screen_settings.display_filter else (255, 255, 255),
                               (screen_settings.native_size[0] / 2, screen_settings.native_size[1] / 2), 10)

        pygame.display.update()

    def handle_mouse_movement(self):
        from settings.settings import screen_settings, fractal_settings

        dx, dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            speed = (0.002 * self.fractal_manager.get_fractal_type().value[1] / self.fractal_manager.zoom)
            self.fractal_manager.center = [self.fractal_manager.center[0] - dx * speed,
                                           self.fractal_manager.center[1] - dy * speed *
                                           (-1 if fractal_settings.fractal_type in [FractalType.SIERPINSKY] else 1)]
            self.fractal_manager.draw(self.screen)

            if screen_settings.display_cursor:
                self.draw_cursor = True
                pygame.draw.circle(self.screen,
                                   screen_settings.filter[::-1] if screen_settings.display_filter else (255, 255, 255),
                                   (screen_settings.native_size[0] / 2, screen_settings.native_size[1] / 2), 10)

            pygame.display.update()

    def run(self):
        from settings.settings import screen_settings

        if self.running:
            raise Exception("The application is already launched")

        self.running = True

        self.fractal_manager.draw(self.screen)
        pygame.display.update()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.zoom_at_cursor(1.1)
                    elif event.button == 5:
                        self.zoom_at_cursor(0.9)
                if event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_movement()

            # remove cursor
            if not pygame.mouse.get_pressed()[0] and self.draw_cursor:
                self.draw_cursor = False
                self.fractal_manager.draw(self.screen)
                pygame.display.update()

            self.clock.tick(screen_settings.fps)

        pygame.quit()
