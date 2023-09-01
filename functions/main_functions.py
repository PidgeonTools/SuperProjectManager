# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Super Project Manager helps you manage your Blender Projects.>
#    Copyright (C) <2023>  <Blender Defender>
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

import bpy
from bpy.utils import previews
from bpy.types import (
    Context
)

import os
from os import path as p

import sys
import subprocess

import json
import time

from .register_functions import (
    register_automatic_folders,
    unregister_automatic_folders,
    register_project_folders
)

from .json_functions import (
    decode_json,
    encode_json,
)

from ..addon_types import AddonPreferences


C = bpy.context
D = bpy.data

BPS_DATA_FILE = p.join(
    p.expanduser("~"),
    "Blender Addons Data",
    "blender-project-starter",
    "BPS.json"
)


def generate_file_version_number(path):
    i = 1
    number = "0001"

    while p.exists("{}_v{}.blend".format(path, number)):
        i += 1
        number = str(i)
        number = "0" * (4 - len(number)) + number

    return "{}_v{}.blend".format(path, number)


def is_file_in_project_folder(context: Context, filepath):
    if filepath == "":
        return False

    filepath = p.normpath(filepath)
    project_folder = p.normpath(p.join(context.scene.project_location,
                                       context.scene.project_name
                                       )
                                )
    return filepath.startswith(project_folder)


def save_filepath(context: Context, filename, subfolder):
    path = p.join(
        context.scene.project_location,
        context.scene.project_name,
        subfolder,
        filename
    ) + ".blend"

    return path


def structure_sets_enum(self, context: Context):
    tooltip = "Select a folder Structure Set."
    items = []

    for i in decode_json(BPS_DATA_FILE)["automatic_folders"]:
        items.append((i, i, tooltip))

    return items


def structure_sets_enum_update(self, context: Context):
    unregister_automatic_folders(self.automatic_folders, self.previous_set)
    register_automatic_folders(
        self.automatic_folders, self.folder_structure_sets)
    self.previous_set = self.folder_structure_sets


def active_project_enum(self, context: Context):
    tooltip = "Select a project you want to work with."
    items = []

    options = decode_json(BPS_DATA_FILE).get("filebrowser_panel_options", [])

    for el in options:
        items.append((el, p.basename(el), tooltip))

    return items


def active_project_enum_update(self: 'AddonPreferences', context: Context):
    register_project_folders(self.project_paths, self.active_project)


def add_unfinished_project(project_path):
    data = decode_json(BPS_DATA_FILE)

    if ["project", project_path] in data["unfinished_projects"]:
        return {'WARNING'}, f"The Project {p.basename(project_path)} already exists in the list of unfinished Projects!"

    data["unfinished_projects"].append(["project", project_path])
    encode_json(data, BPS_DATA_FILE)

    return {'INFO'}, f"Successfully added project {p.basename(project_path)} to the list of unfinished projects."


def finish_project(index):
    data = decode_json(BPS_DATA_FILE)

    data["unfinished_projects"].pop(index)
    encode_json(data, BPS_DATA_FILE)


def write_project_info(root_path, blend_file_path):
    if not blend_file_path.endswith(".blend"):
        return {"WARNING"}, "Can't create a Super Project Manager project! Please select a Blender file and try again."
    data = {
        "blender_files": {
            "main_file": None,
            "other_files": []
        },
    }
    project_info_path = p.join(root_path, ".blender_pm")
    if p.exists(project_info_path):
        data = decode_json(project_info_path)
        set_file_hidden(project_info_path, False)

    bfiles = data["blender_files"]
    if bfiles["main_file"] and bfiles["main_file"] != blend_file_path:
        bfiles["other_files"].append(bfiles["main_file"])
    bfiles["main_file"] = blend_file_path

    ct = time.localtime()  # Current time
    data["build_date"] = [ct.tm_year, ct.tm_mon,
                          ct.tm_mday, ct.tm_hour, ct.tm_min, ct.tm_sec]

    encode_json(data, project_info_path)

    set_file_hidden(project_info_path)

    return {"INFO"}, "Successfully created a Super Project Manager project!"


def set_file_hidden(f, hide_file=True):
    if sys.platform != "win32":
        return

    hide_flag = "+h" if hide_file else "-h"
    subprocess.call(f'attrib {hide_flag} "{f}"', shell=True)
