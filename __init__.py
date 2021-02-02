# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# This addon was created with the Serpens - Visual Scripting Addon.
# This code is generated from nodes and is not intended for manual editing.
# You can find out more about Serpens at <https://blendermarket.com/products/serpens>.


bl_info = {
    "name": "Blender Project Starter",
    "description": "",
    "author": "Steven Scott, Blender Defender",
    "version": (1, 0, 0),
    "blender": (2, 83, 0),
    "location": "Properties >> Scene Properties",
    "warning": "",
    "wiki_url": "https://www.youtube.com/channel/UCiy-QcXrvu9hhe4arymNcfw",
    "tracker_url": "https://github.com/BlenderDefender/blender_project_starter/issues",
    "category": "System"
}


###############   IMPORTS
import bpy
from bpy.utils import previews
import os
import math

from .functions.main_functions import (
    sn_print,
    sn_handle_script_line_exception,
    sn_register_icons,
    sn_register_properties,
    sn_unregister_icons,
    sn_unregister_properties,
)

from . import operators


class BLENDER_PROJECT_STARTER_PT_main_panel(bpy.types.Panel):
    bl_label = "Blender Starter Project"
    bl_idname = "blender_project_starter_PT__main_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 0

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Blender Starter Project panel header")

    def draw(self, context):
        try:
            layout = self.layout

            layout.prop(bpy.context.scene,"project_name",text="Project Name")
            layout.prop(bpy.context.scene,"project_location",text="Project Location")
            layout.prop(bpy.context.scene,"project_setup",text="Project Setup", expand=False,)
            if "Automatic Setup" == bpy.context.scene.project_setup:
                pass
            else:
                layout.label(text="Custom Folder Setup",icon_value=689)
                layout.prop(bpy.context.scene,"folder_1",text="Folder")
                layout.prop(bpy.context.scene,"folder_2",text="Folder 2")
                layout.prop(bpy.context.scene,"folder_3",text="Folder_3")
                layout.prop(bpy.context.scene,"folder_4",text="Folder_4")
                layout.prop(bpy.context.scene,"folder_5",text="Folder_5")
            layout.separator(factor=1.0)

            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            box.label(text=".Blend Save Options",icon_value=70)

            layout.prop(bpy.context.scene,"open_directory",text="Open Folder Window On Build",toggle=False,invert_checkbox=False,)
            layout.prop(bpy.context.scene,"save_blender_file",text="Save .Blend with version number _V001", toggle=False,invert_checkbox=False,)
            if bpy.context.scene.save_blender_file:
                layout.prop(bpy.context.scene,"save_file_name",text="Save File Name")
                row = layout.row(align=False)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.prop(bpy.context.scene,"remap_relative", icon_value = 2,text="Remap Relative")
                row.prop(bpy.context.scene,"compress_save", icon_value = 70,text="Compress File")

            row = layout.row(align=False)
            row.enabled = True
            row.alert = False
            row.scale_x = 2.0
            row.scale_y = 2.0
            op = row.operator("blender_project_starter.build_project",text="BUILD PROJECT", depress=False, icon_value=bpy.context.scene.blender_project_starter_icons["BUILD_ICON"].icon_id)
        except Exception as exc:
            print(str(exc) + " | Error in Blender Starter Project panel")


class BLENDER_PROJECT_STARTER_APT_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_path : bpy.props.StringProperty(name="Default Project Location", subtype="DIR_PATH", default = os.path.expanduser("~")) 
    folder_save1 : bpy.props.StringProperty(name="Folder Name 1", options=set(), default="Blender Files")
    folder_save2 : bpy.props.StringProperty(name="Folder Name 2", options=set(), default= "Textures")
    folder_save3 : bpy.props.StringProperty(name="Folder Name 3", options=set(), default= "Rendered Images")
    folder_save4 : bpy.props.StringProperty(name="Folder Name 4", options=set(), default= "References")
    folder_save5 : bpy.props.StringProperty(name="Folder Name 5", options=set(), default= "Sounds")

    def draw(self, context):

        layout = self.layout
        layout.label(text="Blender Project Manager ",icon_value=bpy.context.scene.blender_project_starter_icons["BUILD_ICON"].icon_id)

        box = layout.box()
        box.enabled = True
        box.alert = False
        box.scale_x = 1.0
        box.scale_y = 1.0
        box.label(text="Blender Project manager ",icon_value=0)
        box.label(text="Here you can setup the automatic project folders ",icon_value=0)
        box.label(text="Format for adding subfolders: Folder>>Subfolder>>Subsubfolder")

        layout.prop(self,"default_path")
        layout.prop(self,"folder_save1")
        layout.prop(self,"folder_save2")
        layout.prop(self,"folder_save3")
        layout.prop(self,"folder_save4")
        layout.prop(self,"folder_save5")
        layout.separator(factor=1.0)


def register():
    operators.register()

    bpy.utils.register_class(BLENDER_PROJECT_STARTER_PT_main_panel)
    bpy.utils.register_class(BLENDER_PROJECT_STARTER_APT_Preferences)

    sn_register_icons()
    sn_register_properties()


def unregister():
    operators.unregister()

    bpy.utils.unregister_class(BLENDER_PROJECT_STARTER_APT_Preferences)
    bpy.utils.unregister_class(BLENDER_PROJECT_STARTER_PT_main_panel)

    sn_unregister_icons()
    sn_unregister_properties()