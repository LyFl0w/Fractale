import time
import pygame
from fractale.fractal import FractalType
from fractale.fractal_manger import FractalManager


class App:
    def __init__(self):
        self.sensitivity = 50
        self.native_size = (600, 600)
        self.fps = 144
        self.target_fps = 30
        self.dt = 0

        self.filtre = (255, 255, 0)
        self.fractal_manager = FractalManager(fractal_type=FractalType.MANDELBROT, size=(500, 500), center=(0, 0),
                                              zoom=0.7,
                                              iteration=20, fractal_power=2)
        self.draw_cursor = False

        self.screen = pygame.display.set_mode(self.native_size)
        self.clock = pygame.time.Clock()

        self.running = False

    def zoom_at_cursor(self, zoom_factor):
        self.fractal_manager.zoom *= zoom_factor
        self.fractal_manager.draw(self.screen, self.native_size, self.filtre)
        if self.draw_cursor:
            pygame.draw.circle(self.screen, self.filtre[::-1], (self.native_size[0] / 2, self.native_size[1] / 2), 10)
        pygame.display.update()

    def handle_mouse_movement(self):
        dx, dy = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[0]:
            self.draw_cursor = True
            speed = (0.0001 * self.sensitivity / self.fractal_manager.zoom)
            self.fractal_manager.center = (self.fractal_manager.center[0] - dx * speed, self.fractal_manager.center[1] - dy * speed)
            self.fractal_manager.draw(self.screen, self.native_size, self.filtre)
            pygame.draw.circle(self.screen, self.filtre[::-1], (self.native_size[0] / 2, self.native_size[1] / 2), 10)
            pygame.display.update()

    def run(self):
        if self.running:
            raise Exception("The application is already launched")

        self.running = True

        self.fractal_manager.draw(self.screen, self.native_size, self.filtre)
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
                self.fractal_manager.draw(self.screen, self.native_size, self.filtre)
                pygame.display.update()

            self.clock.tick(self.fps)

        pygame.quit()
