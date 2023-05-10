#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import os
from os.path import join

# Permet de récupérer le path dynamique de l'application Fracteur

ABSOLUTE_DIR_PATH = os.path.abspath("")

# SETTINGS
SETTINGS_PATH = join(ABSOLUTE_DIR_PATH, "settings")

# SCREENSHOT
SCREENSHOT_PATH = join(ABSOLUTE_DIR_PATH, "screenshot")
