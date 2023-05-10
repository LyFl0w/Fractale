#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


from os.path import exists
from shutil import copy2 as copy

from program.utils.path import SETTINGS_PATH

# Instance statiques des class gérant les paramètres de l'application
screen_settings = None
fractal_settings = None


# Class Mère permettant de créer des paramètres facilement
class Settings:

    # Initialisation des paramètres dess Class filles
    def __init__(self, type_settings):
        # Variable de référence sur la Class fille (variable unique!)
        self.__type_settings = type_settings
        # Création / Chargement du fichier JSON de la Class fille
        self.__create_file()

    # Fonction de référance pour récupérer le chemin du fichier de paramètres
    def __get_path(self, is_default=False) -> str:
        from os.path import join

        return join(join(SETTINGS_PATH, self.__type_settings),
                    ("default_" if is_default else "") + self.__type_settings + "_settings.json")

    def __create_file(self, reset_option=False):
        from program.utils import json_utils

        # Fonction copiant le fichier default..json de la Class fille
        def copy_default_settings():
            default_settings_path = self.__get_path(True)

            # Create DefaultSettings.json if not exist by the base of default variable in the Settings class
            if not exists(default_settings_path):
                # N'écrit par la variable type_settings provenant de cette Class mère
                json_utils.write_json(vars(self), default_settings_path, ["_Settings__type_settings"])

            # Copy DefaultSettings.json inside Settings.json
            copy(default_settings_path, settings_path)

        settings_path = self.__get_path()

        if not exists(settings_path) or reset_option:
            # Create Settings.json if not exist by the base of DefaultSettings.json
            copy_default_settings()

        self.__dict__.update(json_utils.read_json(settings_path))

    # Fonction réinitialisant les paramètres du fichier JSON de la Class fille
    def reset_settings(self):
        self.__create_file(True)

    # Fonction sauvegardant les paramètres du fichier JSON de la Class fille
    def save(self):
        from program.utils import json_utils
        # N'écrit par la variable type_settings provenant de cette Class mère
        json_utils.write_json(vars(self), self.__get_path(), ["_Settings__type_settings"])
