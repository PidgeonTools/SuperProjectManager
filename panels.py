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

from .functions.main_functions import file_in_project_folder


class BLENDER_PROJECT_STARTER_PT_main_panel(bpy.types.Panel):
    bl_label = "Blender Starter Project"
    bl_idname = "blender_project_starter_PT__main_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 0

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Blender Starter Project panel header")

    def draw(self, context):
        try:
            layout = self.layout
            row = layout.row(align=False)
            row.scale_x = 2.0
            row.scale_y = 2.0
            row.operator("blender_project_starter.build_project",
                         text="BUILD PROJECT",
                         depress=False,
                         icon_value=bpy.context.scene.blender_project_starter_icons["BUILD_ICON"].icon_id)

            layout.separator(factor=1.0)

            layout.prop(bpy.context.scene, "project_name", text="Project Name")
            layout.prop(bpy.context.scene, "project_location", text="Project Location")
            layout.prop(bpy.context.scene, "project_setup", text="Project Setup", expand=False,)

            if bpy.context.scene.project_setup == "Custom Setup":
                layout.label(text="Custom Folder Setup", icon_value=689)
                layout.prop(bpy.context.scene, "folder_1", text="Folder")
                layout.prop(bpy.context.scene, "folder_2", text="Folder 2")
                layout.prop(bpy.context.scene, "folder_3", text="Folder_3")
                layout.prop(bpy.context.scene, "folder_4", text="Folder_4")
                layout.prop(bpy.context.scene, "folder_5", text="Folder_5")

            layout.separator(factor=1.0)

            layout.prop(bpy.context.scene, "open_directory", text="Open Directory after Build", expand=False,)

        except Exception as exc:
            print(str(exc) + " | Error in Blender Starter Project panel")


class BLENDER_PROJECT_STARTER_PT_Blender_File_save_options_subpanel(bpy.types.Panel):
    bl_label = "Save .blend File / Options"
    bl_idname = "blender_project_starter_PT_Blender_File_save_options_subpanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_parent_id = "blender_project_starter_PT__main_panel"

    def draw_header(self, context):
        try:
            layout = self.layout
            layout.prop(bpy.context.scene, "save_blender_file", text="")
        except Exception as exc:
            print(str(exc) + " | Error in Blender Starter Project panel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.enabled = bpy.context.scene.save_blender_file

            if bpy.data.filepath == "":
                layout.prop(bpy.context.scene, "file_folder")
                layout.prop(bpy.context.scene, "save_file_name", text="Save File Name")

            elif not file_in_project_folder(context, bpy.data.filepath):
                if context.scene.cut_or_copy:
                    layout.prop(bpy.context.scene, "cut_or_copy", text="Change to Copy File", toggle=True)
                else:
                    layout.prop(bpy.context.scene, "cut_or_copy", text="Change to Cut File", toggle=True)
                layout.prop(bpy.context.scene, "file_folder")
                layout.prop(bpy.context.scene, "save_file_with_new_name", text="Save with new File Name")
                if context.scene.save_file_with_new_name:
                    layout.prop(bpy.context.scene, "save_file_name", text="Save File Name")

            else:
                layout.prop(bpy.context.scene, "save_blender_file_versioned")

            row = layout.row(align=False)

            row.prop(bpy.context.scene, "remap_relative", icon_value=2, text="Remap Relative")
            row.prop(bpy.context.scene, "compress_save", icon_value=70, text="Compress File")

        except Exception as exc:
            print(str(exc) + " | Error in Blender Starter Project panel")


def register():
    bpy.utils.register_class(BLENDER_PROJECT_STARTER_PT_main_panel)
    bpy.utils.register_class(BLENDER_PROJECT_STARTER_PT_Blender_File_save_options_subpanel)


def unregister():
    bpy.utils.unregister_class(BLENDER_PROJECT_STARTER_PT_main_panel)
    bpy.utils.unregister_class(BLENDER_PROJECT_STARTER_PT_Blender_File_save_options_subpanel)
