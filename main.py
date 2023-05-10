#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


from os.path import join

import pygame

from program.application import App
from program.utils import path

if __name__ == "__main__":
    # Initialisation de PyGame
    pygame.init()
    pygame.display.set_caption("Fracteur")
    pygame.display.set_icon(pygame.image.load(join(path.ABSOLUTE_DIR_PATH, "icone.png")))

    # Initialisation et démarrage de l'application
    app = App()
    app.run()
