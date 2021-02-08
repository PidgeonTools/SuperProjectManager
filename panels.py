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

from .functions.main_functions import is_file_in_project_folder

C = bpy.context


class BLENDER_PROJECT_STARTER_PT_main_panel(Panel):
    bl_label = "Blender Starter Project"
    bl_idname = "blender_project_starter_PT__main_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 0

    def draw_header(self, context):
            layout = self.layout

    def draw(self, context):
        prefs = C.preferences.addons[__package__].preferences
        ic = context.scene.blender_project_starter_icons["BUILD_ICON"].icon_id

        layout = self.layout
        row = layout.row(align=False)
        row.scale_x = 2.0
        row.scale_y = 2.0
        row.operator("blender_project_starter.build_project",
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

                op = row.operator("blender_project_starter.remove_folder",
                                  text="",
                                  emboss=False,
                                  icon="PANEL_CLOSE")
                op.index = index
                op.coming_from = "panel"

            row = layout.row()
            split = row.split(factor=0.2)

            split.separator()
            op = split.operator("blender_project_starter.add_folder",
                                icon="PLUS")
            op.coming_from = "panel"

        layout.separator(factor=1.0)

        layout.prop(context.scene,
                    "open_directory",
                    text="Open Directory after Build",
                    expand=False)


class BLENDER_PROJECT_STARTER_PT_Blender_File_save_options_subpanel(Panel):
    bl_label = "Save .blend File / Options"
    bl_idname = "blender_project_starter_PT_Blender_File_save_options_subpanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "blender_project_starter_PT__main_panel"

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene, "save_blender_file")

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


classes = (
    BLENDER_PROJECT_STARTER_PT_main_panel,
    BLENDER_PROJECT_STARTER_PT_Blender_File_save_options_subpanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
