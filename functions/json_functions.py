from os import path as p

import json


def decode_json(path):
    with open(path) as f:
        j = json.load(f)
    return j


def encode_json(j, path):
    with open(path, "w") as f:
        json.dump(j, f, indent=4)
    return j


def get_element(name):
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter",
                  "BPS.json"
                  )

    data = decode_json(path)

    return data[name]
