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
from bpy.props import (
    StringProperty,
    IntProperty,
    EnumProperty
)
from bpy.types import Operator

C = bpy.context

import os
from os import path as p

from .functions.main_functions import (
    build_file_folders,
    generate_file_version_number,
    get_file_subfolder,
    open_directory,
    is_file_in_project_folder,
    save_file,
)

from .functions.json_functions import (
    decode_json,
    encode_json
)

from .functions.register_functions import (
    register_automatic_folders,
    unregister_automatic_folders
)

class BLENDER_PROJECT_STARTER_OT_Build_Project(Operator):
    bl_idname = "blender_project_starter.build_project"
    bl_label = "Build Project"
    bl_description = "Build Project Operator "
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        D = bpy.data
        prefs = C.preferences.addons[__package__].preferences
        path = p.join(context.scene.project_location, context.scene.project_name)
        filename = context.scene.save_file_name

        if not p.isdir(path):
            os.makedirs(path)

        if context.scene.project_setup == "Automatic_Setup":
            for index, folder in enumerate(prefs.automatic_folders):
                try:
                    # print(folder[context.scene.project_setup])
                    build_file_folders(context, folder[context.scene.project_setup])
                except:
                    pass
            subfolder = get_file_subfolder(context.scene.project_setup, prefs.automatic_folders, prefs.save_folder)
        else:
            for index, folder in enumerate(prefs.custom_folders):
                try:
                    # print(folder[context.scene.project_setup])
                    build_file_folders(context, folder[context.scene.project_setup])
                except:
                    pass
            subfolder = get_file_subfolder(context.scene.project_setup, prefs.custom_folders, prefs.save_folder)


        if context.scene.save_blender_file:
            if D.filepath == "":
                save_file(context, filename, subfolder)

            elif not is_file_in_project_folder(context, D.filepath):
                old_file_path = D.filepath

                if context.scene.save_file_with_new_name:
                    save_file(context, filename, subfolder)
                else:
                    save_file(context, p.basename(D.filepath).split(".blend")[0], subfolder)

                if context.scene.cut_or_copy:
                    os.remove(old_file_path)

            elif context.scene.save_blender_file_versioned:
                filepath = p.dirname(D.filepath)
                filename = p.basename(D.filepath).split(".blen")[0].split("_v0")[0]
                version = generate_file_version_number(p.join(filepath, filename))

                filename += version

                save_file(context, filename, subfolder)
            else:
                bpy.ops.wm.save_as_mainfile(filepath=D.filepath, compress=context.scene.compress_save, relative_remap=context.scene.remap_relative)

        if context.scene.open_directory:

                OpenLocation = p.join(context.scene.project_location, context.scene.project_name)
                OpenLocation = p.realpath(OpenLocation)

                open_directory(OpenLocation)

        return {"FINISHED"}


class BLENDER_PROJECT_STARTER_OT_add_folder(Operator):
    bl_idname = "blender_project_starter.add_folder"
    bl_label = "Add Folder"
    bl_description = "Add a Folder with the subfolder Layout Folder>>Subfolder>>Subsubfolder."

    coming_from: StringProperty()

    def execute(self, context):
        pref = context.preferences.addons[__package__].preferences

        if self.coming_from == "prefs":
            folder = pref.automatic_folders.add()

        else:
            folder = pref.custom_folders.add()

        return {"FINISHED"}


class BLENDER_PROJECT_STARTER_OT_remove_folder(Operator):
    bl_idname = "blender_project_starter.remove_folder"
    bl_label = "Remove Folder"
    bl_description = "Remove the selected Folder."

    index: IntProperty()
    coming_from: StringProperty()

    def execute(self, context):
        pref = context.preferences.addons[__package__].preferences

        if self.coming_from == "prefs":
            folder = pref.automatic_folders.remove(self.index)

        else:
            folder = pref.custom_folders.remove(self.index)

        return {"FINISHED"}

classes = (
    BLENDER_PROJECT_STARTER_OT_add_folder,
    BLENDER_PROJECT_STARTER_OT_remove_folder,
    BLENDER_PROJECT_STARTER_OT_Build_Project
)


def register():
    register_automatic_folders(C.preferences.addons[__package__].preferences.automatic_folders)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    unregister_automatic_folders(C.preferences.addons[__package__].preferences.automatic_folders)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
