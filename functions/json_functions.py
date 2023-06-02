from os import path as p

import json

import typing


def decode_json(path: str) -> typing.Union[dict, list]:
    with open(path) as f:
        j = json.load(f)
    return j


def encode_json(j: typing.Union[dict, list], path: str) -> typing.Union[dict, list]:
    with open(path, "w+") as f:
        json.dump(j, f, indent=4)
    return j
