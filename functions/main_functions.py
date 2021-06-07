# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Blender Project Starter is made for automatic Project Folder Generation.>
#    Copyright (C) <2021>  <Steven Scott>
#    Mofified <2021> <Blender Defender>
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

from .json_functions import (
    decode_json,
    encode_json,
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


def build_file_folders(context, prop):

    path = convert_input_to_filepath(context, prop)

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


def open_directory(path):
    if sys.platform == "win32":
        subprocess.call('explorer "{}"'.format(path), shell=True)
    elif sys.platform == "linux":
        subprocess.call('xdg-open "{}"'.format(path), shell=True)
    elif sys.platform == "darwin":
        subprocess.call(["open", path])


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


def get_file_subfolder(options, item):
    try:
        for index, subfolder in enumerate(options):
            if index == int(item):
                return convert_input_to_filepath(input=subfolder.folder_name)
        return ""
    except:
        return ""


def subfolder_enum(self, context):
    tooltip = "Select Folder as target folder for your Blender File. \
Uses Folders from Automatic Setup."
    items = [("Root", "Root", tooltip)]

    folders = self.automatic_folders
    if context.scene.project_setup == "Custom_Setup":
        folders = self.custom_folders
    try:
        for index, folder in enumerate(folders):
            items.append((str(index), folder.folder_name, tooltip))
    except:
        print("Error in main_functions.py, line 128")

    return items


def add_open_project(project_path):
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter",
                  "BPS.json")
    data = decode_json(path)

    data["unfinished_projects"].append(["project", project_path])
    encode_json(data, path)


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
        return {"WARNING"}, "Can't create a Blender PM project! Please select a Blender file and try again."
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

    return {"INFO"}, "Successfully created a Blender PM project!"
