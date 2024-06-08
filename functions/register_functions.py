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
from bpy.props import (
    BoolProperty,
    EnumProperty,
    StringProperty,
)

import os
from os import path as p

import sys
import subprocess

from .json_functions import (
    decode_json,
    encode_json
)

from .. import (
    addon_types,
    __package__
)

C = bpy.context
D = bpy.data
Scene_Prop = bpy.types.Scene

BPS_DATA_FILE = p.join(
    p.expanduser("~"),
    "Blender Addons Data",
    "blender-project-starter",
    "BPS.json"
)


def register_properties():
    prefs: 'addon_types.AddonPreferences' = C.preferences.addons[__package__].preferences

    Scene_Prop.project_name = StringProperty(
        name="Project Name",
        subtype="NONE",
        default="My_Project"
    )
    Scene_Prop.project_location = StringProperty(
        name="Project Location",
        description="Saves the location of file",
        subtype="DIR_PATH",
        default=prefs.default_project_location
    )
    Scene_Prop.project_setup = EnumProperty(
        name="Project Setup",
        items=[
            ("Automatic_Setup", "Automatic Setup", "Automatic Project Setup "),
            ("Custom_Setup", "Custom Setup", "My Custom Setup")
        ]
    )

    Scene_Prop.open_directory = BoolProperty(name="Open Directory",
                                             default=True)
    Scene_Prop.add_new_project = BoolProperty(name="New unfinished project",
                                              default=True)
    Scene_Prop.save_blender_file = BoolProperty(name="Save Blender File",
                                                description="Save Blender \
File on build. If disabled, only the project folders are created",
                                                default=True)

    Scene_Prop.cut_or_copy = BoolProperty(
        name="Cut or Copy",
        description="Decide, if you want to cut or copy your file from the \
current folder to the project folder.",
    )
    Scene_Prop.save_file_with_new_name = BoolProperty(
        name="Save Blender File with another name",
    )
    Scene_Prop.save_blender_file_versioned = BoolProperty(
        name="Add Version Number",
        description="Add a Version Number if the File already exists",
    )
    Scene_Prop.save_file_name = StringProperty(name="Save File Name",
                                               default="My Blend")
    Scene_Prop.remap_relative = BoolProperty(name="Remap Relative",
                                             default=True)
    Scene_Prop.compress_save = BoolProperty(name="Compress Save")
    Scene_Prop.set_render_output = BoolProperty(name="Set the Render Output")

    Scene_Prop.project_rearrange_mode = BoolProperty(
        name="Switch to Rearrange Mode")


def register_automatic_folders(folders, folderset="Default Folder Set"):

    index = 0
    for folder in folders:
        folders.remove(index)

    data = decode_json(BPS_DATA_FILE)

    for folder in data["automatic_folders"][folderset]:
        f = folders.add()
        f["render_outputpath"] = folder[0]
        f["folder_name"] = folder[1]


def unregister_automatic_folders(folders, folderset="Default Folder Set"):
    data = []
    original_json = decode_json(BPS_DATA_FILE)

    for folder in folders:
        data.append([int(folder.render_outputpath),
                     folder.folder_name])

    original_json["automatic_folders"][folderset] = data

    encode_json(original_json, BPS_DATA_FILE)


def register_project_folders(project_folders, project_path):
    project_info: str = p.join(project_path, ".blender_pm")

    index = 0
    for folder in project_folders:
        project_folders.remove(index)

    project_metadata: dict = {}

    if p.exists(project_info):
        project_metadata: dict = decode_json(project_info)

    folders: list = project_metadata.get("displayed_project_folders", [])
    if len(folders) == 0:
        folders = [{"folder_path": f}
                   for f in os.listdir(project_path) if p.isdir(p.join(project_path, f))]

    for folder in folders:
        f = project_folders.add()

        folder_name = p.basename(folder.get("folder_path", ""))
        full_path = p.join(project_path, folder.get("folder_path", ""))

        f["icon"] = folder.get("icon", "FILE_FOLDER")
        f["name"] = folder_name
        f["is_valid"] = p.exists(full_path)
        f["path"] = full_path
