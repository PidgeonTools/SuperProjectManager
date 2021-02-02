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

class BLENDER_PROJECT_STARTER_APT_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_path : bpy.props.StringProperty(name="Default Project Location", subtype="DIR_PATH", default = p.expanduser("~")) 
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
    bpy.utils.register_class(BLENDER_PROJECT_STARTER_APT_Preferences)


def unregister():
    bpy.utils.unregister_class(BLENDER_PROJECT_STARTER_APT_Preferences)
