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


