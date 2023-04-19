from os.path import exists
from shutil import copy2 as copy

from utils.path import DATA_SETTINGS_PATH

screen_settings = None


class Settings:
    def __init__(self, type_settings):
        self.__type_settings = type_settings
        self.__create_file()

    def __get_path(self, is_default=False) -> str:
        from os.path import join

        return join(join(DATA_SETTINGS_PATH, self.__type_settings),
                    ("default_" if is_default else "") + self.__type_settings + "_settings.json")

    def __create_file(self, reset_option=False):
        from utils import json_utils

        def copy_default_player_settings():
            default_player_settings_path = self.__get_path(True)

            # Create DefaultSettings.json if not exist by the base of default variable in the Settings class
            if not exists(default_player_settings_path):
                json_utils.writeJson(vars(self), default_player_settings_path, ["_Settings__type_settings"])

            # Copy DefaultSettings.json inside Settings.json
            copy(default_player_settings_path, settings_path)

        settings_path = self.__get_path()

        if not exists(settings_path) or reset_option:
            # Create Settings.json if not exist by the base of DefaultSettings.json
            copy_default_player_settings()

        self.__dict__.update(json_utils.readJson(settings_path))

    def reset_settings(self):
        self.__create_file(True)

    def save(self):
        from utils import json_utils
        json_utils.writeJson(vars(self), self.__get_path(), ["_Settings__type_settings"])
