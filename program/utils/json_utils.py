#                                                                               
#  Fracteur Copyright (c) 2023 LyFlow and Florely
#  This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#  This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.
#                                                                               


import json
import os
from pathlib import Path

from program.utils.path import SETTINGS_PATH


# Fonction de référance permettant d'écrire facilement des Objets en Json
def write_json(obj, path: str, remove_variable=()):
    # Transform object to dict
    if not isinstance(obj, dict):
        obj = vars(obj)

    # Make a copy of the object so as not to modify the current object
    obj = obj.copy()

    # Remove type variable from object
    for variable in remove_variable:
        if variable in obj.keys():
            del obj[variable]

    # Serializing json
    json_object = json.dumps(obj)

    path = Path(os.path.join(SETTINGS_PATH, path))

    path.parent.mkdir(parents=True, exist_ok=True)

    # Writing to file.json
    with open(path, "w") as outfile:
        outfile.write(json_object)


# Fonction de référance permettant de lire facilement des Objets en format Json
def read_json(json_file_path: str) -> dict:
    # Read JSON file
    data_str = open(os.path.join(SETTINGS_PATH, json_file_path))
    data = json.loads(data_str.read())
    data_str.close()

    return data
