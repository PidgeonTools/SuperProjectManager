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
from bpy.props import (
    StringProperty,
    IntProperty,
    EnumProperty
)
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

import os
from os import path as p

from .functions.main_functions import (
    build_file_folders,
    convert_input_to_filepath,
    generate_file_version_number,
    get_file_subfolder,
    open_directory,
    is_file_in_project_folder,
    save_filepath,
    add_open_project,
    close_project,
    redefine_project_path,
    write_project_info
)

from .functions.json_functions import (
    decode_json,
    encode_json
)

from .functions.register_functions import (
    register_automatic_folders,
    unregister_automatic_folders
)

C = bpy.context


class BLENDER_PROJECT_MANAGER_OT_Build_Project(Operator):
    bl_idname = "blender_project_manager.build_project"
    bl_label = "Build Project"
    bl_description = "Build Project Operator "
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        D = bpy.data
        scene = context.scene
        prefs = C.preferences.addons[__package__].preferences
        projectpath = p.join(context.scene.project_location,
                             context.scene.project_name)
        filename = context.scene.save_file_name

        prefix = ""
        if prefs.prefix_with_project_name:
            prefix = context.scene.project_name + "_"

        folders = prefs.automatic_folders
        if context.scene.project_setup == "Custom_Setup":
            folders = prefs.custom_folders

        is_render_outputfolder_set = [e.render_outputpath for e in folders]
        render_outputfolder = None
        if True in is_render_outputfolder_set:
            render_outputfolder = convert_input_to_filepath(
                context, folders[is_render_outputfolder_set.index(True)].folder_name)
        if not p.isdir(projectpath):
            os.makedirs(projectpath)

        for index, folder in enumerate(folders):
            try:
                build_file_folders(context,
                                   prefix +
                                   folder.folder_name)
            except:
                pass
        subfolder = prefix + \
            get_file_subfolder(folders,
                               prefs.save_folder)

        filepath = D.filepath
        old_filepath = None
        if filepath == "":
            filepath = save_filepath(context, filename, subfolder)
        elif not is_file_in_project_folder(context, D.filepath):
            old_filepath = D.filepath
            filepath = save_filepath(context, filename, subfolder)
            if not context.scene.save_file_with_new_name:
                filepath = save_filepath(context, p.basename(
                    D.filepath).split(".blend")[0], subfolder)
        elif context.scene.save_blender_file_versioned:
            filepath = generate_file_version_number(
                D.filepath.split(".blen")[0].split("_v0")[0])

        # Set the render Output path automatically.
        if prefs.auto_set_render_outputpath and render_outputfolder and context.scene.set_render_output:
            context.scene.render.filepath = "//" + \
                p.relpath(render_outputfolder, p.dirname(filepath)) + "\\"

        if context.scene.save_blender_file:
            bpy.ops.wm.save_as_mainfile(filepath=filepath,
                                        compress=scene.compress_save,
                                        relative_remap=scene.remap_relative
                                        )

            if context.scene.cut_or_copy and old_filepath:
                os.remove(old_filepath)

        if context.scene.add_new_project:
            add_open_project(projectpath)

        write_project_info(projectpath, filepath)

        if context.scene.open_directory:
            OpenLocation = p.join(context.scene.project_location,
                                  context.scene.project_name)
            OpenLocation = p.realpath(OpenLocation)

            open_directory(OpenLocation)

        return {"FINISHED"}


class BLENDER_PROJECT_MANAGER_OT_add_folder(Operator):
    bl_idname = "blender_project_manager.add_folder"
    bl_label = "Add Folder"
    bl_description = "Add a Folder with the subfolder \
Layout Folder>>Subfolder>>Subsubfolder."

    coming_from: StringProperty()

    def execute(self, context):
        pref = context.preferences.addons[__package__].preferences

        if self.coming_from == "prefs":
            folder = pref.automatic_folders.add()

        else:
            folder = pref.custom_folders.add()

        return {"FINISHED"}


class BLENDER_PROJECT_MANAGER_OT_remove_folder(Operator):
    bl_idname = "blender_project_manager.remove_folder"
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


class BLENDER_PROJECT_MANAGER_OT_add_project(Operator, ImportHelper):
    bl_idname = "blender_project_manager.add_project"
    bl_label = "Add Project"
    bl_description = "Add a Project"

    filter_glob: StringProperty(default='*.filterall', options={'HIDDEN'})

    def execute(self, context):
        projectpath = p.dirname(self.filepath)
        add_open_project(projectpath)

        message = "Successfully added project " + p.basename(projectpath)
        self.report({'INFO'}, message)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Please select a project Directory")


class BLENDER_PROJECT_MANAGER_OT_close_project(bpy.types.Operator):
    bl_idname = "blender_project_manager.close_project"
    bl_label = "Close Project"
    bl_description = "Close the selected Project."
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context):
        close_project(self.index)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        # layout.prop(self, "disable")

        layout.label(text="Are you sure?")
        layout.label(
            text="This will remove your project from the open projects list.")

        layout.separator(factor=1)

        layout.label(text="Don't worry, no file gets deleted, ")
        layout.label(
            text="but you might forget about this project and never finish it.")


class BLENDER_PROJECT_MANAGER_OT_redefine_project_path(Operator, ImportHelper):
    bl_idname = "blender_project_manager.redefine_project_path"
    bl_label = "Update Project path"
    bl_description = "Your project has changed location - \
please update the project path"

    name: StringProperty()
    filter_glob: StringProperty(default='*.filterall', options={'HIDDEN'})
    index: IntProperty()

    def execute(self, context):
        projectpath = p.dirname(self.filepath)
        redefine_project_path(self.index, projectpath)

        message = "Successfully changed project path: " + \
            p.basename(projectpath)
        self.report({'INFO'}, message)
        return {"FINISHED"}

    def draw(self, context):
        name = self.name

        layout = self.layout
        layout.label(text="Please select your project Directory for:")
        layout.label(text=name)


class BLENDER_PROJECT_MANAGER_OT_open_project_path(Operator):
    bl_idname = "blender_project_manager.open_project_path"
    bl_label = "Open Project path"
    bl_description = "Open your project folder."

    projectpath: StringProperty()

    def execute(self, context):
        projectpath = self.projectpath
        open_directory(projectpath)
        self.report({'INFO'}, "Opened project path")
        return {"FINISHED"}


class BLENDER_PROJECT_MANAGER_OT_open_blender_file(Operator):
    """Open the latest Blender-File of a project"""
    bl_idname = "blender_project_manager.open_blender_file"
    bl_label = "Open Blender File"
    bl_options = {'REGISTER', 'UNDO'}

    projectpath: StringProperty()

    def execute(self, context):
        project_info = p.join(self.projectpath, ".blender_pm")
        if not p.exists(project_info):
            self.report(
                {"WARNING"}, "Your project is not a Blender PM Project.")
            # MESSAGE (Dialog for Project info): Convert the project into a Blender PM Project. Don't worry,
            # this won't delete or overwrite any Files.
            # TODO: Open a dialog, to convert the Folder into a Blender Project. Store the .blender_pm file in the given root folder
            # and let the User pick the location of the Blender File.
            # Edge Case: Only allow files that end with .blend

            return {'FINISHED'}

        if self.path_to_blend():
            bpy.ops.wm.open_mainfile(filepath=self.path_to_blend())
            return {"FINISHED"}

        self.report(
            {"ERROR"}, "No Blender File found in this project! Please select the latest project file.")
        # TODO: Insert a function that Updates the Blender PM Info File with the latest Blender File.
        return {'FINISHED'}

    # Return the path to the latest Blender File. If the latest
    def path_to_blend(self):
        blender_files = decode_json(
            p.join(self.projectpath, ".blender_pm"))["blender_files"]
        filepath = blender_files["main_file"]
        if p.exists(filepath):
            self.report(
                {"INFO"}, "Opened the project file found in {}".format(filepath))
            return filepath

        for filepath in blender_files["other_files"][::-1]:
            if p.exists(filepath):
                self.report(
                    {"WARNING"}, "The latest File is unavailable. Opening the newest version available: {}".format(filepath))
                return filepath

        return


classes = (
    BLENDER_PROJECT_MANAGER_OT_add_folder,
    BLENDER_PROJECT_MANAGER_OT_remove_folder,
    BLENDER_PROJECT_MANAGER_OT_Build_Project,
    BLENDER_PROJECT_MANAGER_OT_add_project,
    BLENDER_PROJECT_MANAGER_OT_close_project,
    BLENDER_PROJECT_MANAGER_OT_redefine_project_path,
    BLENDER_PROJECT_MANAGER_OT_open_project_path,
    BLENDER_PROJECT_MANAGER_OT_open_blender_file
)


def register():
    folders = C.preferences.addons[__package__].preferences.automatic_folders
    register_automatic_folders(folders)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    folders = C.preferences.addons[__package__].preferences.automatic_folders
    unregister_automatic_folders(folders)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
