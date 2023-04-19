import json
import os
from utils.path import *
from pathlib import Path


def writeJson(obj, path: str, remove_variable=()):
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

    path = Path(os.path.join(DATA_PATH, path))

    path.parent.mkdir(parents=True, exist_ok=True)

    # Writing to file.json
    with open(path, "w") as outfile:
        outfile.write(json_object)


def readJson(json_file_path: str) -> dict:
    # Read JSON file
    data_str = open(os.path.join(DATA_PATH, json_file_path))
    data = json.loads(data_str.read())
    data_str.close()

    return data
