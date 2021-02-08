# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Blender Project Starter is an addon for automatic Project Folder Structure Generation.>
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
C = bpy.context
D = bpy.data

import os
from os import path as p

import sys
import subprocess

import json

from .json_functions import (
    decode_json,
    encode_json,
    get_element
)


def build_file_folders(context, prop):

    prop = prop.split(">>")
    path = p.join(context.scene.project_location, context.scene.project_name)

    for i in prop:
        path = p.join(path, i)

    if not p.isdir(path):
        os.makedirs(path)


def generate_file_version_number(path):
    i = 1

    while p.exists(path + "_v" + str(i / 10000).split(".")[1] + ".blend"):
        i += 1

    return "_v" + str(i / 10000).split(".")[1]


def open_directory(path):
    if sys.platform == "win32":
        subprocess.call('explorer "{}"'.format(path), shell=True)
    elif sys.platform == "linux":
        subprocess.call('xdg-open "{}"'.format(path), shell=True)
    elif sys.platform == "darwin":
        subprocess.call('open "{}"'.format(path), shell=True)


def is_file_in_project_folder(context, filepath):
    if filepath == "":
        return False

    filepath = p.normpath(filepath)
    project_folder = p.normpath(p.join(context.scene.project_location, context.scene.project_name))
    return filepath.startswith(project_folder)


def save_file(context, filename, subfolder):
    bpy.ops.wm.save_as_mainfile(
        filepath=p.join(
            context.scene.project_location,
            context.scene.project_name,
            subfolder,
            filename
        ) + ".blend",
        compress=context.scene.compress_save,
        relative_remap=context.scene.remap_relative
    )


def get_file_subfolder(context, options, item):
    try:
        for index, subfolder in enumerate(options):
            if index == int(item):
                prop = subfolder[context].split(">>")
                subfolder = ""
                for i in prop:
                    subfolder = p.join(subfolder, i)
                return subfolder
        return ""
    except:
        return ""


def subfolder_enum():
    tooltip = "Select Folder as target folder for your Blender File. Uses Folders from Automatic Setup. If you choose an invalid folder, the Root Folder will be selected."
    default = [("Root", "Root", tooltip)]
    index = 0

    try:
        for folder in get_element("automatic_folders"):
            default.append((str(index), folder, tooltip))
            index += 1
    except:
        return default

    return default
