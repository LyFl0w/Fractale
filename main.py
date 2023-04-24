from os.path import join

import pygame
from program.application import App
from program.utils import path

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Fracteur")
    pygame.display.set_icon(pygame.image.load(join(path.ABSOLUTE_DIR_PATH, "icone.png")))

    app = App()
    app.run()
