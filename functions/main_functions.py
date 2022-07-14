# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Blender Project Starter is made for automatic Project Folder Generation.>
#    Copyright (C) <2021>  <Steven Scott>
#    Modified <2021> <Blender Defender>
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

import os
from os import path as p

import sys
import subprocess

import json
import time

from .register_functions import (
    register_automatic_folders,
    unregister_automatic_folders
)

from .json_functions import (
    decode_json,
    encode_json,
)

from .path_generator import (
    Subfolders
)

C = bpy.context
D = bpy.data


def convert_input_to_filepath(context=None, input=""):
    parts = input.split(">>")
    path = ""
    if context:
        path = p.join(context.scene.project_location,
                      context.scene.project_name)

    for i in parts:
        path = p.join(path, i)

    return path


def build_file_folders(context, prefix, unparsed_string):

    for path in Subfolders(unparsed_string).paths:
        top_level_path = p.join(context.scene.project_location,
                                context.scene.project_name)
        path = prefix + path
        path = p.join(top_level_path, path)

        if not p.isdir(path):
            os.makedirs(path)


def generate_file_version_number(path):
    i = 1
    number = "0001"

    while p.exists("{}_v{}.blend".format(path, number)):
        i += 1
        number = str(i)
        number = "0" * (4 - len(number)) + number

    return "{}_v{}.blend".format(path, number)


def is_file_in_project_folder(context, filepath):
    if filepath == "":
        return False

    filepath = p.normpath(filepath)
    project_folder = p.normpath(p.join(context.scene.project_location,
                                       context.scene.project_name
                                       )
                                )
    return filepath.startswith(project_folder)


def save_filepath(context, filename, subfolder):
    path = p.join(
        context.scene.project_location,
        context.scene.project_name,
        subfolder,
        filename
    ) + ".blend"

    return path


def subfolder_enum(self, context):
    tooltip = "Select Folder as target folder for your Blender File. \
Uses Folders from Automatic Setup."
    items = [("Root", "Root", tooltip)]

    folders = self.automatic_folders
    if context.scene.project_setup == "Custom_Setup":
        folders = self.custom_folders
    try:
        for folder in folders:
            for folder in Subfolders(folder.folder_name).display_paths:
                items.append((folder, folder, tooltip))
    except:
        print("Error in main_functions.py, line 128")

    return items


def structure_sets_enum(self, context):
    tooltip = "Select a folder Structure Set."
    items = []

    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter",
                  "BPS.json")

    for i in decode_json(path)["automatic_folders"]:
        items.append((i, i, tooltip))

    return items


def structure_sets_enum_update(self, context):
    unregister_automatic_folders(self.automatic_folders, self.previous_set)
    register_automatic_folders(
        self.automatic_folders, self.folder_structure_sets)
    self.previous_set = self.folder_structure_sets


def add_unfinished_project(project_path):
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter",
                  "BPS.json")
    data = decode_json(path)

    if ["project", project_path] in data["unfinished_projects"]:
        return {'WARNING'}, f"The Project {p.basename(project_path)} already exists in the list of unfinished Projects!"

    data["unfinished_projects"].append(["project", project_path])
    encode_json(data, path)

    return {'INFO'}, f"Successfully added project {p.basename(project_path)} to the list of unfinished projects."


def close_project(index):
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter",
                  "BPS.json")
    data = decode_json(path)

    data["unfinished_projects"].pop(index)
    encode_json(data, path)


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
        if sys.platform == "win32":
            subprocess.call(
                'attrib -h "{}"'.format(project_info_path), shell=True)

    bfiles = data["blender_files"]
    if bfiles["main_file"] and bfiles["main_file"] != blend_file_path:
        bfiles["other_files"].append(bfiles["main_file"])
    bfiles["main_file"] = blend_file_path

    ct = time.localtime()  # Current time
    data["build_date"] = [ct.tm_year, ct.tm_mon,
                          ct.tm_mday, ct.tm_hour, ct.tm_min, ct.tm_sec]

    encode_json(data, project_info_path)

    if sys.platform == "win32":
        subprocess.call('attrib +h "{}"'.format(project_info_path), shell=True)

    return {"INFO"}, "Successfully created a Super Project Manager project!"
