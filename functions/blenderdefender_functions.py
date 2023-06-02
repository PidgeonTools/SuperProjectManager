# ##### BEGIN GPL LICENSE BLOCK #####
#
# <Blender Defender Utility Functions>
#  Copyright (C) <2021>  <Blender Defender>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import os
from os import path as p

import json

import time

import shutil

from .json_functions import (
    decode_json,
    encode_json
)


def setup_addons_data():
    """Setup and validate the addon data."""
    default_addons_data = {
        "automatic_folders": {
            "Default Folder Set": [
                [
                    0,
                    "Blender Files"
                ],
                [
                    1,
                    "Images>>Textures++References++Rendered Images"
                ],
                [
                    0,
                    "Sounds"
                ]
            ]
        },
        "unfinished_projects": [],
        "version": 130
    }

    addons_data_path = p.join(
        p.expanduser("~"),
        "Blender Addons Data",
        "blender-project-starter"
    )
    addons_data_file = p.join(addons_data_path, "BPS.json")

    if not p.isdir(addons_data_path):
        os.makedirs(addons_data_path)

    if "BPS.json" not in os.listdir(addons_data_path):
        encode_json(default_addons_data, addons_data_file)

    addons_data = ""
    try:
        addons_data = decode_json(addons_data_file)
    except Exception:
        pass

    if type(addons_data) != dict:
        shutil.move(addons_data_file, p.join(addons_data_path,
                                             f"BPS.{time.strftime('%Y-%m-%d')}.json"))
        encode_json(default_addons_data, addons_data_file)
        addons_data = default_addons_data

    if addons_data.get("version") < 130:
        encode_json(update_json(addons_data), addons_data_file)


def update_to_120(data):
    data["version"] = 120
    return data


def update_to_130(data):
    default_folders = []
    while data["automatic_folders"]:
        folder = data["automatic_folders"].pop(0)
        default_folders.append([False, folder])

    data["automatic_folders"] = {}
    data["automatic_folders"]["Default Folder Set"] = default_folders

    for i in range(len(data["unfinished_projects"])):
        data["unfinished_projects"][i] = [
            "project", data["unfinished_projects"][i]]

    data["version"] = 130

    return data


def update_json(data: dict) -> dict:
    version = data.get("version", 110)

    if version == 110:
        data = update_to_120(data)
        version = 120

    if version == 120:
        data = update_to_130(data)
        version = 130

    return data
