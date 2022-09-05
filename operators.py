# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Blender Project Starter is made for automatic Project Folder Generation.>
#    Copyright (C) <2021>  <Steven Scott>
#    Modified <2021> <Blender Defender>
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
from bpy.types import (
    Context,
    Event,
    UILayout,
    Operator
)

from bpy_extras.io_utils import ImportHelper

import os
from os import path as p

from .functions.main_functions import (
    build_file_folders,
    convert_input_to_filepath,
    generate_file_version_number,
    is_file_in_project_folder,
    save_filepath,
    add_unfinished_project,
    finish_project,
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

from .functions.path_generator import (
    Subfolders
)

C = bpy.context


class SUPER_PROJECT_MANAGER_OT_Build_Project(Operator):
    bl_idname = "super_project_manager.build_project"
    bl_label = "Build Project"
    bl_description = "Build Project Operator "
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: Context):

        D = bpy.data
        scene = context.scene
        prefs = C.preferences.addons[__package__].preferences
        projectpath = p.join(context.scene.project_location,
                             context.scene.project_name)
        filename = context.scene.save_file_name

        # Set the prefix.
        prefix = ""
        if prefs.prefix_with_project_name:
            prefix = context.scene.project_name + "_"

        # Set the list of Subfolders.
        folders = prefs.automatic_folders
        if context.scene.project_setup == "Custom_Setup":
            folders = prefs.custom_folders

        # Set the render outputfolder FULL path.
        is_render_outputfolder_set = [e.render_outputpath for e in folders]
        render_outputfolder = None

        if True in is_render_outputfolder_set:
            unparsed_string = folders[is_render_outputfolder_set.index(
                True)].folder_name
            output_path = prefix + Subfolders(
                unparsed_string).paths[-1]  # Use last path.
            render_outputfolder = convert_input_to_filepath(
                context, output_path)

        # Create the Project Folder.
        if not p.isdir(projectpath):
            os.makedirs(projectpath)

        # Build all Project Folders
        for folder in folders:
            try:
                build_file_folders(context,
                                   prefix,
                                   folder.folder_name)
            except:
                pass

        # Set the subfolder of the Blender file.
        subfolder = prefix + convert_input_to_filepath(input=prefs.save_folder)
        if prefs.save_folder == "Root":
            subfolder = ""

        # Set the path the Blender File gets saved to.
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

        # Add the project to the list of unfinished projects.
        if context.scene.add_new_project:
            add_unfinished_project(projectpath)

        # Store all the necessary data in the project info file
        write_project_info(projectpath, filepath)

        # Open the project directory in the explorer, if wanted.
        if context.scene.open_directory:
            open_location = p.join(context.scene.project_location,
                                   context.scene.project_name)
            open_location = p.realpath(open_location)

            bpy.ops.wm.path_open(filepath=open_location)

        return {"FINISHED"}


class SUPER_PROJECT_MANAGER_OT_add_folder(Operator):
    bl_idname = "super_project_manager.add_folder"
    bl_label = "Add Folder"
    bl_description = "Add a Folder with the subfolder \
Layout Folder>>Subfolder>>Subsubfolder."

    coming_from: StringProperty()

    def execute(self, context: Context):
        pref = context.preferences.addons[__package__].preferences

        if self.coming_from == "prefs":
            folder = pref.automatic_folders.add()

        else:
            folder = pref.custom_folders.add()

        return {"FINISHED"}


class SUPER_PROJECT_MANAGER_OT_remove_folder(Operator):
    bl_idname = "super_project_manager.remove_folder"
    bl_label = "Remove Folder"
    bl_description = "Remove the selected Folder."

    index: IntProperty()
    coming_from: StringProperty()

    def execute(self, context: Context):
        pref = context.preferences.addons[__package__].preferences

        if self.coming_from == "prefs":
            folder = pref.automatic_folders.remove(self.index)

        else:
            folder = pref.custom_folders.remove(self.index)

        return {"FINISHED"}


class SUPER_PROJECT_MANAGER_OT_add_project(Operator, ImportHelper):
    bl_idname = "super_project_manager.add_project"
    bl_label = "Add Project"
    bl_description = "Add a Project"

    filter_glob: StringProperty(default='*.filterall', options={'HIDDEN'})

    def execute(self, context: Context):
        projectpath = p.dirname(self.filepath)

        message_type, message = add_unfinished_project(projectpath)
        self.report(message_type, message)
        return {"FINISHED"}

    def draw(self, context: Context):
        layout = self.layout
        layout.label(text="Please select a project Directory")


class SUPER_PROJECT_MANAGER_OT_finish_project(bpy.types.Operator):
    bl_idname = "super_project_manager.finish_project"
    bl_label = "Finish Project"
    bl_description = "Finish the selected Project."
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()
    project_name: StringProperty()

    def execute(self, context: Context):
        finish_project(self.index)
        return {'FINISHED'}

    def invoke(self, context: Context, event: Event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: Context):
        layout: UILayout = self.layout
        # layout.prop(self, "disable")

        layout.label(
            text="Hurray, you've fininished your project!", icon="FUND")
        layout.label(
            text=f"Click OK below to remove '{self.project_name}' from your ToDo List.")


class SUPER_PROJECT_MANAGER_OT_redefine_project_path(Operator, ImportHelper):
    bl_idname = "super_project_manager.redefine_project_path"
    bl_label = "Update Project path"
    bl_description = "Your project has changed location - \
please update the project path"

    name: StringProperty()
    filter_glob: StringProperty(default='*.filterall', options={'HIDDEN'})
    index: IntProperty()

    def execute(self, context: Context):
        projectpath = p.dirname(self.filepath)
        self.redefine_project_path(self.index, projectpath)

        message = "Successfully changed project path: " + \
            p.basename(projectpath)
        self.report({'INFO'}, message)
        return {"FINISHED"}

    def draw(self, context: Context):
        name = self.name

        layout = self.layout
        layout.label(text="Please select your project Directory for:")
        layout.label(text=name)

    def redefine_project_path(self, index, new_path):
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["unfinished_projects"][index][1] = new_path
        encode_json(data, path)


class SUPER_PROJECT_MANAGER_OT_open_blender_file(Operator):
    """Open the latest Blender-File of a project"""
    bl_idname = "super_project_manager.open_blender_file"
    bl_label = "Open Blender File"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty()
    message_type: StringProperty()
    message: StringProperty()

    def execute(self, context: Context):

        bpy.ops.wm.open_mainfile(filepath=self.filepath)
        self.report(
            {self.message_type}, self.message)
        return {"FINISHED"}


class SUPER_PROJECT_MANAGER_ot_define_blend_file_location(bpy.types.Operator, ImportHelper):
    """This Operator is used to (re)define the location of the projects main Blender File"""
    bl_idname = "super_project_manager.define_blend_file_location"
    bl_label = "Define Project Blender File Path"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Can't find the right path to the Blender File. \
Please select the latest Blender File of you Project."

    filter_glob: StringProperty(default='*.blend', options={'HIDDEN'})
    message_type: StringProperty()
    message: StringProperty()
    projectpath: StringProperty()

    def execute(self, context: Context):
        # print(self.filepath)
        write_project_info(self.projectpath, self.filepath)

        message = "Successfully defined Blender Filepath: " + \
            p.basename(self.filepath)
        self.report({'INFO'}, message)

        bpy.ops.super_project_manager.open_blender_file(
            filepath=self.filepath, message_type="INFO", message=f"Opened the project file found in {self.filepath}")
        return {"FINISHED"}

    def draw(self, context: Context):
        name = p.basename(self.projectpath)

        layout = self.layout
        layout.label(text=self.message_type + ": " + self.message)
        layout.label(text="Please select your project Directory for:")
        layout.label(text=name)


class SUPER_PROJECT_MANAGER_ot_rearrange_up(bpy.types.Operator):
    """Rearrange a Project or Label one step up."""
    bl_idname = "super_project_manager.rearrange_up"
    bl_label = "Rearrange Up"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context: Context):
        index = self.index
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["unfinished_projects"][index], data["unfinished_projects"][index -
                                                                        1] = data["unfinished_projects"][index - 1], data["unfinished_projects"][index]

        encode_json(data, path)
        return {'FINISHED'}


class SUPER_PROJECT_MANAGER_ot_rearrange_down(bpy.types.Operator):
    """Rearrange a Project or Label one step down."""
    bl_idname = "super_project_manager.rearrange_down"
    bl_label = "Rearrange Down"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context: Context):
        index = self.index
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["unfinished_projects"][index], data["unfinished_projects"][index +
                                                                        1] = data["unfinished_projects"][index + 1], data["unfinished_projects"][index]

        encode_json(data, path)
        return {'FINISHED'}


class SUPER_PROJECT_MANAGER_ot_rearrange_to_top(bpy.types.Operator):
    """Rearrange a Project or Label to the top."""
    bl_idname = "super_project_manager.rearrange_to_top"
    bl_label = "Rearrange to Top"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context: Context):
        index = self.index
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        element = data["unfinished_projects"].pop(index)

        data["unfinished_projects"].insert(0, element)

        encode_json(data, path)
        return {'FINISHED'}


class SUPER_PROJECT_MANAGER_ot_rearrange_to_bottom(bpy.types.Operator):
    """Rearrange a Project or Label to the bottom."""
    bl_idname = "super_project_manager.rearrange_to_bottom"
    bl_label = "Rearrange to Bottom"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context: Context):
        index = self.index
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        element = data["unfinished_projects"].pop(index)

        data["unfinished_projects"].append(element)

        encode_json(data, path)
        return {'FINISHED'}


class SUPER_PROJECT_MANAGER_ot_add_label(bpy.types.Operator):
    """Add a category Label to the open projects list."""
    bl_idname = "super_project_manager.add_label"
    bl_label = "Add Label"
    bl_options = {'REGISTER', 'UNDO'}

    label: StringProperty()

    def execute(self, context: Context):
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["unfinished_projects"].append(["label", self.label])

        encode_json(data, path)
        return {'FINISHED'}

    def invoke(self, context: Context, event: Event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: Context):
        layout: UILayout = self.layout

        layout.prop(self, "label", text="Category Label Text:")


class SUPER_PROJECT_MANAGER_ot_remove_label(bpy.types.Operator):
    """Remove a category Label from the open projects list."""
    bl_idname = "super_project_manager.remove_label"
    bl_label = "Remove Label"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context: Context):
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["unfinished_projects"].pop(self.index)

        encode_json(data, path)
        return {'FINISHED'}


class SUPER_PROJECT_MANAGER_ot_change_label(bpy.types.Operator):
    """Change a category Label from the open projects list."""
    bl_idname = "super_project_manager.change_label"
    bl_label = "Change Label"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()
    label: StringProperty()

    def execute(self, context: Context):
        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["unfinished_projects"][self.index] = ["label", self.label]

        encode_json(data, path)
        return {'FINISHED'}

    def invoke(self, context: Context, event: Event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: Context):
        layout: UILayout = self.layout

        layout.prop(self, "label", text="Category Label Text:")


class SUPER_PROJECT_MANAGER_ot_add_structure_set(bpy.types.Operator):
    """Adds a new folder structure set."""
    bl_idname = "super_project_manager.add_structure_set"
    bl_label = "Add Folder Structure Set"
    bl_options = {'REGISTER', 'UNDO'}

    name: StringProperty()

    def execute(self, context: Context):
        prefs = context.preferences.addons[__package__].preferences

        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["automatic_folders"][self.name] = []

        encode_json(data, path)

        prefs.folder_structure_sets = self.name

        return {'FINISHED'}

    def invoke(self, context: Context, event: Event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: Context):
        layout = self.layout

        layout.prop(self, "name", text="Folder Structure Set Name:")


class SUPER_PROJECT_MANAGER_ot_remove_structure_set(bpy.types.Operator):
    """Remove a folder structure set"""
    bl_idname = "super_project_manager.remove_structure_set"
    bl_label = "Remove Set"
    bl_options = {'REGISTER', 'UNDO'}

    structure_set: StringProperty()

    def execute(self, context: Context):
        prefs = context.preferences.addons[__package__].preferences
        prefs.folder_structure_sets = "Default Folder Set"

        if self.structure_set == "Default Folder Set":
            return {'FINISHED'}

        path = p.join(p.expanduser("~"),
                      "Blender Addons Data",
                      "blender-project-starter",
                      "BPS.json")
        data = decode_json(path)

        data["automatic_folders"].pop(self.structure_set)

        encode_json(data, path)

        return {'FINISHED'}


classes = (
    SUPER_PROJECT_MANAGER_OT_add_folder,
    SUPER_PROJECT_MANAGER_OT_remove_folder,
    SUPER_PROJECT_MANAGER_OT_Build_Project,
    SUPER_PROJECT_MANAGER_OT_add_project,
    SUPER_PROJECT_MANAGER_OT_finish_project,
    SUPER_PROJECT_MANAGER_OT_redefine_project_path,
    SUPER_PROJECT_MANAGER_OT_open_blender_file,
    SUPER_PROJECT_MANAGER_ot_define_blend_file_location,
    SUPER_PROJECT_MANAGER_ot_rearrange_up,
    SUPER_PROJECT_MANAGER_ot_rearrange_down,
    SUPER_PROJECT_MANAGER_ot_rearrange_to_top,
    SUPER_PROJECT_MANAGER_ot_rearrange_to_bottom,
    SUPER_PROJECT_MANAGER_ot_add_label,
    SUPER_PROJECT_MANAGER_ot_remove_label,
    SUPER_PROJECT_MANAGER_ot_change_label,
    SUPER_PROJECT_MANAGER_ot_add_structure_set,
    SUPER_PROJECT_MANAGER_ot_remove_structure_set
)


def register():
    prefs = C.preferences.addons[__package__].preferences
    register_automatic_folders(prefs.automatic_folders, prefs.previous_set)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    prefs = C.preferences.addons[__package__].preferences
    unregister_automatic_folders(prefs.automatic_folders, prefs.previous_set)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
