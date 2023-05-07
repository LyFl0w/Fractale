#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#


import threading
import tkinter as tk

import pygame

from program import interface
from program.prototype import cube3d, pyramide3d
from program.fractal.fractal_manger import FractalManager
from program.fractal.fractalbase import FractalType
from program.settings.fractal_settings import FractalSettings
from program.settings.screen_settings import ScreenSettings
from program.utils import queue_update


class App:
    def __init__(self):
        ScreenSettings()
        FractalSettings()

        from program.settings.settingsbase import screen_settings

        self.screen = pygame.display.set_mode(screen_settings.get_native_size())
        self.clock = pygame.time.Clock()

        self.running = False
        self.draw_cursor = False
        self.moving = False

        self.__queue_update = queue_update.QueueUpdate(self)

        self.fractal_manager = FractalManager(zoom=0.5)

        self.cube3D_running, self.pyramide3D_running = False, False

    def zoom_at_cursor(self, zoom_factor):
        from program.settings.settingsbase import screen_settings

        self.set_moving()
        self.fractal_manager.zoom *= zoom_factor
        self.draw_fractal()
        if self.draw_cursor:
            pygame.draw.circle(self.screen,
                               screen_settings.filter[::-1] if screen_settings.display_filter else (255, 255, 255),
                               (screen_settings.get_native_size()[0] / 2, screen_settings.get_native_size()[1] / 2), 10)

        if interface.entry_z is not None:
            interface.entry_z.config(textvariable=tk.DoubleVar(value=round(self.fractal_manager.zoom, 3)))

        pygame.display.update()

    def handle_mouse_movement(self):
        from program.settings.settingsbase import screen_settings, fractal_settings

        dx, dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            self.set_moving()
            speed = ((
                             0.002 * self.fractal_manager.get_fractal_type().default_sensibility * screen_settings.sensibility) / (
                             self.fractal_manager.zoom * 5))
            self.fractal_manager.center = [self.fractal_manager.center[0] - dx * speed,
                                           self.fractal_manager.center[1] - dy * speed *
                                           (-1 if fractal_settings.fractal_type in [
                                               FractalType.SIERPINSKI.name] else 1)]
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
                    if event.key == pygame.K_c and not self.cube3D_running:
                        threading.Thread(target=cube3d.run, args=(self,)).start()
                    if event.key == pygame.K_b and not self.pyramide3D_running:
                        threading.Thread(target=pyramide3d.run, args=(self,)).start()

            # remove cursor
            if not pygame.mouse.get_pressed()[0]:
                self.set_not_moving()
                if self.draw_cursor:
                    self.draw_cursor = False
                    self.draw_fractal()
                    pygame.display.update()
            else:
                if interface.entry_x is not None:
                    interface.entry_x.config(textvariable=tk.DoubleVar(value=self.fractal_manager.center[0]))

                if interface.entry_y is not None:
                    interface.entry_y.config(textvariable=tk.DoubleVar(value=self.fractal_manager.center[1]))

            self.clock.tick(screen_settings.fps)

        if interface.root is not None:
            interface.kill_thread()

        pygame.quit()

    def add_element_to_queue(self, key):
        self.__queue_update.put(key)

    def draw_fractal(self):
        self.fractal_manager.draw(self.screen)

    def set_moving(self):
        if not self.moving:
            self.moving = True
            self.fractal_manager.update_downsampling(0.8)

    def set_not_moving(self):
        if self.moving:
            self.moving = False
            self.fractal_manager.update_downsampling(1)
