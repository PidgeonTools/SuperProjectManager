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
import os
from os import path as p

from .functions.main_functions import (
    sn_handle_script_line_exception,
    build_folder,
    version_number,
    file_subfolder,
    open_directory
)


class BLENDER_PROJECT_STARTER_OT_Build_Project(bpy.types.Operator):
    bl_idname = "blender_project_starter.build_project"
    bl_label = "Build Project"
    bl_description = "Build Project Operator "
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            if "Automatic Setup" == bpy.context.scene.project_setup:
                prefs = context.preferences.addons[__package__].preferences

                build_folder(context, prefs.folder_1)

                if prefs.folder_2:
                    build_folder(context, prefs.folder_2)

                if prefs.folder_3:
                    build_folder(context, prefs.folder_3)

                if prefs.folder_4:
                    build_folder(context, prefs.folder_4)

                if prefs.folder_5:
                    build_folder(context, prefs.folder_5)

                subfolder = file_subfolder(bpy.context.scene.file_folder, prefs)

            else:
                scene = bpy.context.scene

                build_folder(context, scene.folder_1)

                if scene.folder_2:
                    build_folder(context, scene.folder_2)

                if scene.folder_3:
                    build_folder(context, scene.folder_3)

                if scene.folder_4:
                    build_folder(context, scene.folder_4)

                if scene.folder_5:
                    build_folder(context, scene.folder_5)

                subfolder = file_subfolder(bpy.context.scene.file_folder, bpy.context.scene)

            if bpy.context.scene.save_blender_file:
                if bpy.data.filepath == "":
                    bpy.ops.wm.save_as_mainfile(
                        filepath=p.join(
                            bpy.context.scene.project_location,
                            bpy.context.scene.project_name,
                            subfolder,
                            bpy.context.scene.save_file_name
                        ) + ".blend",
                        compress=bpy.context.scene.compress_save,
                        relative_remap=bpy.context.scene.remap_relative
                    )
                elif bpy.context.scene.save_blender_file_versioned:
                    filename = bpy.data.filepath.split("//")
                    filename = filename[len(filename) - 1].split(".blen")[0].split("_v")[0]
                    version = version_number(filename)
                    bpy.ops.wm.save_as_mainfile(filepath=filename + version + ".blend", compress=bpy.context.scene.compress_save, relative_remap=bpy.context.scene.remap_relative)
                else:
                    filename = bpy.data.filepath.split("//")
                    filename = filename[len(filename) - 1]
                    bpy.ops.wm.save_as_mainfile(filepath=filename, compress=bpy.context.scene.compress_save, relative_remap=bpy.context.scene.remap_relative)

            if bpy.context.scene.open_directory:
                try:
                    OpenLocation = bpy.path.abspath(p.join(bpy.context.scene.project_location, bpy.context.scene.project_name))
                except Exception as exc:
                    sn_handle_script_line_exception(exc, ("OpenLocation =  '" + bpy.path.abspath(p.join(bpy.context.scene.project_location, bpy.context.scene.project_name))))

                try:
                    OpenLocation = p.realpath(OpenLocation)

                except Exception as exc:
                    sn_handle_script_line_exception(exc, "OpenLocation = os.path.realpath(OpenLocation)")

                try:
                    open_directory(OpenLocation)
                except Exception as exc:
                    sn_handle_script_line_exception(exc, "os.startfile(OpenLocation)")

        except Exception as exc:
            print(str(exc) + " | Error in execute function of Build Project")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Build Project")
        return self.execute(context)


def register():
    bpy.utils.register_class(BLENDER_PROJECT_STARTER_OT_Build_Project)


def unregister():
    bpy.utils.unregister_class(BLENDER_PROJECT_STARTER_OT_Build_Project)
