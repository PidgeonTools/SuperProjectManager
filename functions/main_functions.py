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

import os
from os import path as p

import sys
import subprocess


def build_folder(context, prop):
    try:
        prop = prop.split(">>")
        path = p.join(bpy.path.abspath(bpy.context.scene.project_location), bpy.context.scene.project_name)

        for i in prop:
            path = p.join(path, i)

    except Exception as exc:
        handle_script_line_exception(
            exc,
            ("path ='" + bpy.path.abspath(p.join(bpy.path.abspath(bpy.context.scene.project_location, bpy.context.scene.project_name), prop)))
        )

    if not p.isdir(path):
        os.makedirs(path)


def version_number(path):
    i = 1

    while p.exists(path + "_v" + str(i / 10000).split(".")[1] + ".blend"):
        i += 1

    return "_v" + str(i / 10000).split(".")[1]


def file_subfolder(options, context):
    if options == "Root":
        return ""
    elif options == "Folder 1":
        return context.folder_1
    elif options == "Folder 2":
        return context.folder_2
    elif options == "Folder 3":
        return context.folder_3
    elif options == "Folder 4":
        return context.folder_4
    elif options == "Folder 5":
        return context.folder_5


def open_directory(path):
    if sys.platform == "win32":
        subprocess.call('explorer "{}"'.format(path), shell=True)
    elif sys.platform == 'linux':
        subprocess.call('xdg-open "{}"'.format(path), shell=True)
    elif sys.platform == 'darwin':
        subprocess.call('open "{}"'.format(path), shell=True)


def file_in_project_folder(context, filepath):
    if filepath == "":
        return False

    project_folder = p.normpath(p.join(context.scene.project_location, context.scene.project_name))
    filepath = p.normpath(filepath)
    return filepath.startswith(project_folder)


def copy_file(context, filename, subfolder):
    bpy.ops.wm.save_as_mainfile(
        filepath=p.join(
            bpy.context.scene.project_location,
            bpy.context.scene.project_name,
            subfolder,
            filename
        ) + ".blend",
        compress=bpy.context.scene.compress_save,
        relative_remap=bpy.context.scene.remap_relative
    )

def handle_script_line_exception(exc, line):
    print("# # # # # # # # SCRIPT LINE ERROR # # # # # # # #")
    print("Line:", line)
    raise exc


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

    bpy.types.Scene.project_name = bpy.props.StringProperty(
        name="Project Name",
        subtype="NONE",
        default="My_Project"
    )
    bpy.types.Scene.project_location = bpy.props.StringProperty(
        name="Project Location",
        description="Saves the location of file",
        subtype="DIR_PATH",
        default=prefs.default_path
    )
    bpy.types.Scene.project_setup = bpy.props.EnumProperty(
        name="Project Setup",
        items=[
            ("Automatic Setup", "Automatic Setup", "Automatic Project Setup "),
            ("Custom Setup", "Custom Setup", "My Custom Setup")
        ]
    )

    bpy.types.Scene.folder_1 = bpy.props.StringProperty(name="Folder_1", description="Custom Folder Setup")
    bpy.types.Scene.folder_2 = bpy.props.StringProperty(name="Folder_2", description="Folder Structure 2 ")
    bpy.types.Scene.folder_3 = bpy.props.StringProperty(name="Folder_3", description="Custom Folder 3 ")
    bpy.types.Scene.folder_4 = bpy.props.StringProperty(name="Folder_4", description="Custom Folder 4")
    bpy.types.Scene.folder_5 = bpy.props.StringProperty(name="Folder_5", description="Custom Folder 5")

    bpy.types.Scene.open_directory = bpy.props.BoolProperty(name="Open Directory", options=set(), default=True)
    bpy.types.Scene.save_blender_file = bpy.props.BoolProperty(name="Save Blender File", options=set(), default=True)
    bpy.types.Scene.file_folder = bpy.props.EnumProperty(
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


    bpy.types.Scene.cut_or_copy = bpy.props.BoolProperty(
        name="Cut or Copy",
        description="Decide, if you want to cut or copy your file from the current folder to the project folder.",
        default=False
    )
    bpy.types.Scene.save_file_with_new_name = bpy.props.BoolProperty(
        name="Save Blender File with another name",
        default=False
    )
    bpy.types.Scene.save_blender_file_versioned = bpy.props.BoolProperty(
        name="Add Version Number",
        description="Add a Version Number if the File already exists",
        default=False
    )
    bpy.types.Scene.save_file_name = bpy.props.StringProperty(name="Save File Name")
    bpy.types.Scene.remap_relative = bpy.props.BoolProperty(name="Remap Relative", default=True)
    bpy.types.Scene.compress_save = bpy.props.BoolProperty(name="Compress Save", default=False)
