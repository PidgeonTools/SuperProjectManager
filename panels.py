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
from bpy.types import Panel

import os
from os import path as p

from .functions.main_functions import is_file_in_project_folder

from .functions.json_functions import decode_json

C = bpy.context


class BLENDER_PROJECT_MANAGER_PT_main_panel(Panel):
    bl_label = "Blender Project Manager"
    bl_idname = "blender_project_manager_PT__main_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 0

    def draw(self, context):
        pass


class BLENDER_PROJECT_MANAGER_PT_starter_main_panel(Panel):
    bl_label = "Project Starter"
    bl_idname = "blender_project_manager_PT_starter_main_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "blender_project_manager_PT__main_panel"

    def draw_header(self, context):
            layout = self.layout

    def draw(self, context):
        prefs = C.preferences.addons[__package__].preferences
        ic = context.scene.blender_project_manager_icons["BUILD_ICON"].icon_id

        layout = self.layout
        row = layout.row(align=False)
        row.scale_x = 2.0
        row.scale_y = 2.0
        row.operator("blender_project_manager.build_project",
                     text="BUILD PROJECT",
                     icon_value=ic)

        layout.separator(factor=1.0)

        layout.prop(context.scene,
                    "project_name",
                    text="Project Name")
        layout.prop(context.scene,
                    "project_location",
                    text="Project Location")
        layout.prop(context.scene,
                    "project_setup",
                    text="Project Setup",
                    expand=False)

        if context.scene.project_setup == "Custom_Setup":
            layout.label(text="Custom Folder Setup",
                         icon="NEWFOLDER")

            for index, folder in enumerate(prefs.custom_folders):
                row = layout.row()
                split = row.split(factor=0.2)
                split.label(text="Folder {}".format(index + 1))

                split.prop(folder, "Custom_Setup", text="")

                op = row.operator("blender_project_manager.remove_folder",
                                  text="",
                                  emboss=False,
                                  icon="PANEL_CLOSE")
                op.index = index
                op.coming_from = "panel"

            row = layout.row()
            split = row.split(factor=0.2)

            split.separator()
            op = split.operator("blender_project_manager.add_folder",
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


class BLENDER_PROJECT_MANAGER_PT_Blender_File_save_options_subpanel(Panel):
    bl_label = " "
    bl_idname = "blender_project_manager_PT_Blender_File_save_options_subpanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "blender_project_manager_PT_starter_main_panel"

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene, "save_blender_file", text="Save Blender File / Options")

    def draw(self, context):
        D = bpy.data
        prefs = C.preferences.addons[__package__].preferences

        layout = self.layout
        layout.enabled = context.scene.save_blender_file

        if D.filepath == "":
            layout.prop(prefs, "save_folder")
            layout.prop(context.scene, "save_file_name", text="Save File Name")

        elif not is_file_in_project_folder(context, D.filepath):
            if context.scene.cut_or_copy:
                layout.prop(context.scene,
                            "cut_or_copy",
                            text="Change to Copy File",
                            toggle=True)
            else:
                layout.prop(context.scene,
                            "cut_or_copy",
                            text="Change to Cut File",
                            toggle=True)
            layout.prop(prefs, "save_folder")
            layout.prop(context.scene,
                        "save_file_with_new_name",
                        text="Save with new File Name")
            if context.scene.save_file_with_new_name:
                layout.prop(context.scene,
                            "save_file_name",
                            text="Save File Name")
        else:
            layout.prop(context.scene, "save_blender_file_versioned")

        row = layout.row(align=False)
        row.prop(context.scene,
                 "remap_relative",
                 icon="ERROR",
                 text="Remap Relative")
        row.prop(context.scene,
                 "compress_save",
                 icon="FILE_TICK",
                 text="Compress File")


class BLENDER_PROJECT_MANAGER_PT_Open_Projects_subpanel(Panel):
    bl_label = "Project Manager"
    bl_idname = "blender_project_manager_PT_Open_Projects_subpanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "blender_project_manager_PT__main_panel"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Here are your unfinished projects:")
        path = p.join(p.expanduser("~"),
                    "Blender Addons Data",
                    "blender-project-starter",
                    "BPS.json")
        data = decode_json(path)["unfinished_projects"]

        if len(data) == 0:
            url = "https://www.brograph.com/randorender"

            layout.separator(factor=0.25)
            layout.label(text="Nothing to do.", icon="CHECKMARK")
            layout.operator("wm.url_open", text="Find a project idea").url=url
            layout.separator(factor=0.75)

        for index, project in enumerate(data):
            project_name = p.basename(project)

            row = layout.row()

            row.label(text=project_name)
            op = row.operator("blender_project_manager.open_project_path",
                            text="",
                            emboss=False,
                            icon="WORKSPACE")
            op.path = project

            op = row.operator("blender_project_manager.close_project",
                            text="",
                            emboss=False,
                            icon="PANEL_CLOSE")
            op.index = index

            if not p.exists(project):
                op = row.operator("blender_project_manager.redefine_project_path",
                                text="",
                                icon="ERROR")
                op.index = index
                op.name = project_name

        layout.operator("blender_project_manager.add_project",
                        text="Add unfinished project",
                        icon="PLUS")


classes = (
    BLENDER_PROJECT_MANAGER_PT_main_panel,
    BLENDER_PROJECT_MANAGER_PT_starter_main_panel,
    BLENDER_PROJECT_MANAGER_PT_Blender_File_save_options_subpanel,
    BLENDER_PROJECT_MANAGER_PT_Open_Projects_subpanel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
