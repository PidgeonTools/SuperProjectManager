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

# import operators
import bpy
from bpy.types import (
    Context,
    Panel,
    UILayout,
)

import os
from os import path as p

from .addon_types import AddonPreferences

from .functions.main_functions import is_file_in_project_folder

from .functions.json_functions import decode_json

C = bpy.context

BPS_DATA_FILE = p.join(
    p.expanduser("~"),
    "Blender Addons Data",
    "blender-project-starter",
    "BPS.json"
)


class SUPER_PROJECT_MANAGER_PT_main_panel(Panel):
    bl_label = "Super Project Manager"
    bl_idname = "super_project_manager_PT__main_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 0

    def draw(self, context: Context):
        pass


class SUPER_PROJECT_MANAGER_PT_starter_main_panel(Panel):
    bl_label = "Project Starter"
    bl_idname = "super_project_manager_PT_starter_main_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "super_project_manager_PT__main_panel"

    def draw(self, context: Context):
        prefs: 'AddonPreferences' = C.preferences.addons[__package__].preferences

        layout: UILayout = self.layout

        # Project Name Property
        row = layout.row()
        row.label(text="Project Name")

        row = layout.row()
        row.prop(context.scene,
                 "project_name",
                 text="")

        layout.separator(factor=0.5)

        # Project Location Property
        row = layout.row()
        row.label(text="Project Location")

        row = layout.row()
        row.prop(context.scene,
                 "project_location",
                 text="")

        layout.separator(factor=0.5)

        # Layout all options for saving the Blender File.
        layout.prop(context.scene, "save_blender_file",
                    text="Save Blender File")
        if context.scene.save_blender_file:
            self.draw_file_options(context)

        layout.separator(factor=2.0)

        # Project Setup (Automatic/Manual)
        row = layout.row()
        row.label(text="Project Setup")
        row = layout.row()
        row.prop(context.scene,
                 "project_setup",
                 text="",
                 expand=False)

        if context.scene.project_setup == "Custom_Setup":
            box = layout.box()
            box.label(text="Custom Folder Setup",
                      icon="NEWFOLDER")

            render_outpath_active = True in [
                e.render_outputpath for e in prefs.custom_folders]

            for index, folder in enumerate(prefs.custom_folders):
                row = box.row()

                # Folder Name
                row.prop(folder, "folder_name", text="")

                # Render Output
                if prefs.auto_set_render_outputpath:
                    col = row.column()
                    col.enabled = folder.render_outputpath or not render_outpath_active
                    col.prop(folder, "render_outputpath",
                             text="", icon="OUTPUT", emboss=folder.render_outputpath)

                # Remove button
                op = row.operator("super_project_manager.remove_folder",
                                  text="",
                                  emboss=False,
                                  icon="PANEL_CLOSE")
                op.index = index
                op.coming_from = "panel"

            row = box.row()
            op = row.operator("super_project_manager.add_folder",
                              icon="PLUS")
            op.coming_from = "panel"

        layout.separator(factor=1.0)

        layout.prop(context.scene,
                    "add_new_project",
                    text="Add project to unfinished projects list.",
                    expand=False)

        layout.prop(context.scene,
                    "open_directory",
                    text="Open Directory after Build",
                    expand=False)

        # Build Project Button
        row = layout.row(align=False)
        row.scale_x = 2.0
        row.scale_y = 2.0
        row.operator("super_project_manager.build_project",
                     text="Build Project")  # , icon_value=ic)

    def draw_file_options(self, context: Context):
        D = bpy.data
        prefs: 'AddonPreferences' = C.preferences.addons[__package__].preferences

        layout: UILayout = self.layout
        layout.enabled = context.scene.save_blender_file

        box = layout.box()

        if D.filepath == "":
            # File Name
            row = box.row()
            row.label(text="File Name")
            row = box.row()
            row.prop(context.scene, "save_file_name", text="")

            # Subdirectory
            row = box.row()
            row.label(text="Subdirectory")
            row = box.row()
            row.prop(prefs, "save_folder", text="")

        elif not is_file_in_project_folder(context, D.filepath):
            if context.scene.cut_or_copy:
                box.prop(context.scene,
                         "cut_or_copy",
                         text="Change to Copy File",
                         toggle=True)
            else:
                box.prop(context.scene,
                         "cut_or_copy",
                         text="Change to Cut File",
                         toggle=True)
            box.prop(prefs, "save_folder")
            box.prop(context.scene,
                     "save_file_with_new_name",
                     text="Save with new File Name")
            if context.scene.save_file_with_new_name:
                box.prop(context.scene,
                         "save_file_name",
                         text="Save File Name")
        else:
            box.prop(context.scene, "save_blender_file_versioned")

        box.separator()

        box.label(text="Further options:")

        # Remap relative
        row = box.row(align=False)
        row.prop(context.scene,
                 "remap_relative",
                 text="Remap Relative")

        # Compress file
        row = box.row(align=False)
        row.prop(context.scene,
                 "compress_save",
                 text="Compress File")

        # Automatically set the render output.
        if prefs.auto_set_render_outputpath:
            row = box.row()
            row.prop(context.scene,
                     "set_render_output",
                     icon="OUTPUT",
                     text="Set Render Output")


class SUPER_PROJECT_MANAGER_PT_Open_Projects_subpanel(Panel):
    bl_label = "Project Manager"
    bl_idname = "super_project_manager_PT_Open_Projects_subpanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "super_project_manager_PT__main_panel"

    def draw(self, context: Context):
        layout: UILayout = self.layout

        data = decode_json(BPS_DATA_FILE)["unfinished_projects"]

        project_count = len([e for e in data if e[0] == "project"])
        layout.label(
            text="Here are your {} unfinished projects:".format(project_count))

        if project_count == 0:
            url = "https://bd-links.netlify.app/randorender"

            layout.separator(factor=0.25)
            layout.label(text="Nothing to do.", icon="CHECKMARK")
            layout.operator(
                "wm.url_open", text="Find a project idea").url = url
            layout.separator(factor=0.75)

        elif context.scene.project_rearrange_mode:
            self.draw_rearrange(context, data)
            layout.operator("super_project_manager.add_label",
                            text="Add Category Label",
                            icon="PLUS")
            layout.prop(context.scene, "project_rearrange_mode",
                        text="Switch to Project Display", toggle=True)
        else:
            self.draw_normal(context, data)
            layout.prop(context.scene, "project_rearrange_mode",
                        text="Switch to Rearrange Mode", toggle=True)

        layout.operator("super_project_manager.add_project",
                        text="Add unfinished project",
                        icon="PLUS")

    # Return the path to the latest Blender File.
    # If the latest Blender File is unavailable, the path to an older File
    # is returned. If no file is available, None is returned.
    def path_to_blend(self, projectpath):
        if not p.exists(p.join(projectpath, ".blender_pm")):
            return None, "WARNING", "Your project is not a Super Project Manager Project."

        blender_files = decode_json(
            p.join(projectpath, ".blender_pm"))["blender_files"]
        filepath = blender_files["main_file"]
        if p.exists(filepath):
            # self.report(
            #     {"INFO"}, "Opened the project file found in {}".format(filepath))
            return filepath, "INFO", "Opened the project file found in {}".format(filepath)

        for filepath in blender_files["other_files"][::-1]:
            if p.exists(filepath):
                # self.report(
                #     {"WARNING"}, "The latest File is unavailable. Opening the newest version available: {}".format(filepath))
                return filepath, "WARNING", "The latest File is unavailable. Opening the newest version available: {}".format(filepath)

        return None, "ERROR", "No Blender File found in this project! Please select the latest project file."

    # Drawing Function for the regular project display mode.
    def draw_normal(self, context: Context, data):
        layout: UILayout = self.layout

        for index, entry in enumerate(data):
            type = entry[0]
            content = entry[1]

            if type == "project":
                project = content
                project_name = p.basename(project)

                row = layout.row()

                row.label(text=project_name)

                if not p.exists(project):
                    op = row.operator("super_project_manager.redefine_project_path",
                                      text="",
                                      icon="ERROR")
                    op.index = index
                    op.name = project_name

                operator = "super_project_manager.open_blender_file"
                if not self.path_to_blend(project)[0]:
                    operator = "super_project_manager.define_blend_file_location"
                op = row.operator(operator,
                                  text="",
                                  emboss=False,
                                  icon="BLENDER")
                project_details = self.path_to_blend(project)
                if project_details[0]:
                    op.filepath = project_details[0]
                else:
                    op.projectpath = project
                op.message_type = project_details[1]
                op.message = project_details[2]

                op = row.operator("wm.path_open",
                                  text="",
                                  emboss=False,
                                  icon="FOLDER_REDIRECT")
                op.filepath = project

                op = row.operator("super_project_manager.finish_project",
                                  text="",
                                  emboss=False,
                                  icon="CHECKMARK")
                op.index = index
                op.project_name = project_name

            if type == "label":
                label = content
                row = layout.row()
                row.label(text="")
                row = layout.row()
                row.label(text=label)

    # Drawing Function for the project rearrange mode.
    def draw_rearrange(self, context: Context, data):
        layout: UILayout = self.layout

        for index, entry in enumerate(data):
            type = entry[0]
            content = entry[1]

            content = p.basename(content)
            row = layout.row()
            row.label(text=content)

            if type == "label":
                op = row.operator("super_project_manager.remove_label",
                                  text="",
                                  emboss=False,
                                  icon="PANEL_CLOSE")
                op.index = index
                op = row.operator("super_project_manager.change_label",
                                  text="",
                                  emboss=False,
                                  icon="FILE_TEXT")
                op.index = index

            op = row.operator("super_project_manager.rearrange_to_top",
                              text="",
                              emboss=False,
                              icon="EXPORT")
            op.index = index

            op = row.operator("super_project_manager.rearrange_up",
                              text="",
                              emboss=False,
                              icon="SORT_DESC")
            op.index = index

            op = row.operator("super_project_manager.rearrange_down",
                              text="",
                              emboss=False,
                              icon="SORT_ASC")
            op.index = index

            op = row.operator("super_project_manager.rearrange_to_bottom",
                              text="",
                              emboss=False,
                              icon="IMPORT")
            op.index = index


classes = (
    SUPER_PROJECT_MANAGER_PT_main_panel,
    SUPER_PROJECT_MANAGER_PT_starter_main_panel,
    # SUPER_PROJECT_MANAGER_PT_Blender_File_save_options_subpanel,
    SUPER_PROJECT_MANAGER_PT_Open_Projects_subpanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
