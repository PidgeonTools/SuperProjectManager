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
    StringProperty,
    EnumProperty
)

import os
from os import path as p

import sys
import subprocess

from .json_functions import (
    decode_json,
    encode_json
)

C = bpy.context
D = bpy.data
Scene_Prop = bpy.types.Scene


def register_icons():
    icons = ["BUILD_ICON", "TWITTER", "YOUTUBE", "GUMROAD"]
    Scene_Prop.super_project_manager_icons = previews.new()
    icons_dir = p.join(p.dirname(p.dirname(__file__)), "icons")
    for icon in icons:
        Scene_Prop.super_project_manager_icons.load(icon,
                                                    p.join(icons_dir,
                                                           icon + ".png"),
                                                    "IMAGE")


def unregister_icons():
    previews.remove(Scene_Prop.super_project_manager_icons)


def register_properties():
    prefs = C.preferences.addons[__package__.split(".")[0]].preferences

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
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter", "BPS.json")

    index = 0
    for folder in folders:
        folders.remove(index)

    data = decode_json(path)

    for folder in data["automatic_folders"][folderset]:
        f = folders.add()
        f["render_outputpath"] = folder[0]
        f["folder_name"] = folder[1]


def unregister_automatic_folders(folders, folderset="Default Folder Set"):
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter",
                  "BPS.json")
    data = []
    original_json = decode_json(path)

    for folder in folders:
        data.append([int(folder.render_outputpath),
                     folder.folder_name])

    original_json["automatic_folders"][folderset] = data

    encode_json(original_json, path)
