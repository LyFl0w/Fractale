import pygame

from fractale.fractal import FractalType
from fractale.fractal_manger import FractalManager
from settings.screen_settings import ScreenSettings


class App:
    def __init__(self):
        ScreenSettings()

        self.fractal_manager = FractalManager(fractal_type=FractalType.SIERPINSKY, size=[800, 800], center=[0, 0],
                                              zoom=0.5, iteration=6, fractal_power=2)

        from settings.settings import screen_settings

        self.screen = pygame.display.set_mode(screen_settings.native_size)
        self.clock = pygame.time.Clock()

        self.running = False

    def zoom_at_cursor(self, zoom_factor):
        from settings.settings import screen_settings

        self.fractal_manager.zoom *= zoom_factor
        self.fractal_manager.draw(self.screen, screen_settings.native_size, screen_settings.filter)
        if screen_settings.draw_cursor:
            pygame.draw.circle(self.screen, screen_settings.filter[::-1],
                               (screen_settings.native_size[0] / 2, screen_settings.native_size[1] / 2), 10)
        pygame.display.update()

    def handle_mouse_movement(self):
        from settings.settings import screen_settings

        dx, dy = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            screen_settings.draw_cursor = True
            speed = (0.001 * self.fractal_manager.fractal_type.value[1] * 50 / self.fractal_manager.zoom)
            self.fractal_manager.center = [
                self.fractal_manager.center[0] - dx * speed, self.fractal_manager.center[1] - dy * speed]
            self.fractal_manager.draw(self.screen, screen_settings.native_size, screen_settings.filter)
            pygame.draw.circle(self.screen, screen_settings.filter[::-1], (screen_settings.native_size[0] / 2, screen_settings.native_size[1] / 2), 10)
            pygame.display.update()

    def run(self):
        from settings.settings import screen_settings

        if self.running:
            raise Exception("The application is already launched")

        self.running = True

        self.fractal_manager.draw(self.screen, screen_settings.native_size, screen_settings.filter)
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
            if not pygame.mouse.get_pressed()[0] and screen_settings.draw_cursor:
                screen_settings.draw_cursor = False
                self.fractal_manager.draw(self.screen, screen_settings.native_size, screen_settings.filter)
                pygame.display.update()

            self.clock.tick(screen_settings.fps)

        pygame.quit()
