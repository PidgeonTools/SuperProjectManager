# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Blender Project Starter is an addon for automatic Project Folder Structure Generation.>
#    Copyright (C) <2021>  <Steven Scott>
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


def register_icons():
    icons = ["BUILD_ICON", "TWITTER", "YOUTUBE", "GUMROAD"]
    bpy.types.Scene.blender_project_starter_icons = previews.new()
    icons_dir = p.join(p.dirname(p.dirname(__file__)), "icons")
    for icon in icons:
        bpy.types.Scene.blender_project_starter_icons.load(icon, p.join(icons_dir, icon + ".png"), "IMAGE")


def unregister_icons():
    previews.remove(bpy.types.Scene.blender_project_starter_icons)


def register_properties():
    prefs = bpy.context.preferences.addons[__package__.split(".")[0]].preferences

    bpy.types.Scene.project_name = StringProperty(
        name="Project Name",
        subtype="NONE",
        default="My_Project"
    )
    bpy.types.Scene.project_location = StringProperty(
        name="Project Location",
        description="Saves the location of file",
        subtype="DIR_PATH",
        default=prefs.default_path
    )
    bpy.types.Scene.project_setup = EnumProperty(
        name="Project Setup",
        items=[
            ("Automatic Setup", "Automatic Setup", "Automatic Project Setup "),
            ("Custom Setup", "Custom Setup", "My Custom Setup")
        ]
    )

    bpy.types.Scene.folder_1 = StringProperty(name="Folder_1", description="Custom Folder Setup")
    bpy.types.Scene.folder_2 = StringProperty(name="Folder_2", description="Folder Structure 2 ")
    bpy.types.Scene.folder_3 = StringProperty(name="Folder_3", description="Custom Folder 3 ")
    bpy.types.Scene.folder_4 = StringProperty(name="Folder_4", description="Custom Folder 4")
    bpy.types.Scene.folder_5 = StringProperty(name="Folder_5", description="Custom Folder 5")

    bpy.types.Scene.open_directory = BoolProperty(name="Open Directory", default=True)
    bpy.types.Scene.save_blender_file = BoolProperty(name="Save Blender File",
                                                     description="Save Blender File on build. If disable"
                                                     + "d, only the project folders are created",
                                                     default=True)
    bpy.types.Scene.file_folder = EnumProperty(
        name="Folder",
        items=[
            ("Root", "Root", "Save to Root Folder"),
            ("Folder 1", prefs.folder_1, "Save to Folder 1"),
            ("Folder 2", prefs.folder_2, "Save to Folder 2"),
            ("Folder 3", prefs.folder_3, "Save to Folder 3"),
            ("Folder 4", prefs.folder_4, "Save to Folder 4"),
            ("Folder 5", prefs.folder_5, "Save to Folder 5")
        ]
    )

    bpy.types.Scene.cut_or_copy = BoolProperty(
        name="Cut or Copy",
        description="Decide, if you want to cut or copy your file from the current folder to the project folder.",
    )
    bpy.types.Scene.save_file_with_new_name = BoolProperty(
        name="Save Blender File with another name",
    )
    bpy.types.Scene.save_blender_file_versioned = BoolProperty(
        name="Add Version Number",
        description="Add a Version Number if the File already exists",
    )
    bpy.types.Scene.save_file_name = StringProperty(name="Save File Name")
    bpy.types.Scene.remap_relative = BoolProperty(name="Remap Relative", default=True)
    bpy.types.Scene.compress_save = BoolProperty(name="Compress Save")
