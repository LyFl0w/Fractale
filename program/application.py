from program import interface
from program.fractal.fractalbase import FractalType
from program.utils import queue_update
import threading

import pygame

from program.fractal.fractal_manger import FractalManager
from program.settings.fractal_settings import FractalSettings
from program.settings.screen_settings import ScreenSettings


class App:
    def __init__(self):
        ScreenSettings()
        FractalSettings()

        from program.settings.settingsbase import screen_settings

        self.screen = pygame.display.set_mode(screen_settings.get_native_size())
        self.clock = pygame.time.Clock()

        self.running = False
        self.draw_cursor = False

        self.__queue_update = queue_update.QueueUpdate(self)

        self.fractal_manager = FractalManager(zoom=0.5)

    def zoom_at_cursor(self, zoom_factor):
        from program.settings.settingsbase import screen_settings

        self.fractal_manager.zoom *= zoom_factor
        self.draw_fractal()
        if self.draw_cursor:
            pygame.draw.circle(self.screen,
                               screen_settings.filter[::-1] if screen_settings.display_filter else (255, 255, 255),
                               (screen_settings.get_native_size()[0] / 2, screen_settings.get_native_size()[1] / 2), 10)

        pygame.display.update()

    def handle_mouse_movement(self):
        from program.settings.settingsbase import screen_settings, fractal_settings

        dx, dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            speed = ((0.002 * self.fractal_manager.get_fractal_type().default_sensibility * screen_settings.sensibility) / (self.fractal_manager.zoom * 5))
            self.fractal_manager.center = [self.fractal_manager.center[0] - dx * speed,
                                           self.fractal_manager.center[1] - dy * speed *
                                           (1 if fractal_settings.fractal_type in [FractalType.SIERPINSKY] else 1)]
            self.draw_fractal()

            if screen_settings.display_cursor:
                self.draw_cursor = True
                pygame.draw.circle(self.screen,
                                   screen_settings.filter[::-1] if screen_settings.display_filter else (255, 255, 255),
                                   (screen_settings.get_native_size()[0] / 2, screen_settings.get_native_size()[1] / 2),
                                   10)

            pygame.display.update()

    def run(self):
        from program.settings.settingsbase import screen_settings

        if self.running:
            raise Exception("The application is already launched")

        self.running = True

        self.draw_fractal()
        pygame.display.update()

        while self.running:
            self.__queue_update.execute()

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if interface.root is None:
                            # Démarrer le thread Tkinter uniquement s'il n'est pas déjà en cours d'exécution
                            threading.Thread(target=interface.run, args=(self,)).start()

            # remove cursor
            if not pygame.mouse.get_pressed()[0] and self.draw_cursor:
                self.draw_cursor = False
                self.draw_fractal()
                pygame.display.update()

            self.clock.tick(screen_settings.fps)

        if interface.root is not None:
            interface.kill_thread()

        pygame.quit()

    def add_element_to_queue(self, key):
        self.__queue_update.put(key)

    def draw_fractal(self):
        self.fractal_manager.draw(self.screen)
