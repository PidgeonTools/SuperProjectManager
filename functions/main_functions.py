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
from bpy.utils import previews

import os
from os import path as p

def build_folder(context, prop):
    try:
        prop = prop.replace(">>", "\\")
        path = os.path.join(bpy.path.abspath(bpy.context.scene.project_location), bpy.context.scene.project_name, prop)

    except Exception as exc:
        sn_handle_script_line_exception(exc, ("path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location, bpy.context.scene.project_name), prop))))

    if not os.path.isdir(path):
        os.makedirs(path)



def sn_print(tree_name, *args):
    if tree_name in bpy.data.node_groups:
        item = bpy.data.node_groups[tree_name].sn_graphs[0].prints.add()
        for arg in args:
            item.value += str(arg) + ";;;"
        for area in bpy.context.screen.areas:
            area.tag_redraw()
    print(*args)


def sn_handle_script_line_exception(exc, line):
    print("# # # # # # # # SCRIPT LINE ERROR # # # # # # # #")
    print("Line:", line)
    raise exc

###############   REGISTER ICONS
def sn_register_icons():
    icons = ["BUILD_ICON","TWITTER","YOUTUBE","GUMROAD",]
    bpy.types.Scene.blender_project_starter_icons = bpy.utils.previews.new()
    icons_dir = os.path.join( os.path.dirname( __file__ ), "icons" )
    for icon in icons:
        bpy.types.Scene.blender_project_starter_icons.load( icon, os.path.join( icons_dir, icon + ".png" ), "IMAGE" )

def sn_unregister_icons():
    bpy.utils.previews.remove( bpy.types.Scene.blender_project_starter_icons )


###############   REGISTER PROPERTIES
def sn_register_properties():
    prefs = bpy.context.preferences.addons[__package__.split(".")[0]].preferences

    bpy.types.Scene.project_name = bpy.props.StringProperty(name="Project Name", subtype="NONE", options=set(), default="My_Project")
    bpy.types.Scene.project_location = bpy.props.StringProperty(name="Project Location", description="Saves the location of file", subtype="DIR_PATH", options=set(), default= prefs.default_path)
    bpy.types.Scene.project_setup = bpy.props.EnumProperty(name="Project Setup", options=set(),items=[("Automatic Setup", "Automatic Setup", "Automatic Project Setup "), ("Custom Setup", "Custom Setup", "My Custom Setup")])

    bpy.types.Scene.folder_1 = bpy.props.StringProperty(name="Folder_1", description="Custom Folder Setup", options=set())
    bpy.types.Scene.folder_2 = bpy.props.StringProperty(name="Folder_2", description="Folder Structure 2 ", options=set())
    bpy.types.Scene.folder_3 = bpy.props.StringProperty(name="Folder_3", description="Custom Folder 3 ", options=set())
    bpy.types.Scene.folder_4 = bpy.props.StringProperty(name="Folder_4", description="Custom Folder 4", options=set())
    bpy.types.Scene.folder_5 = bpy.props.StringProperty(name="Folder_5", description="Custom Folder 5", options=set())

    bpy.types.Scene.open_directory = bpy.props.BoolProperty(name="Open Directory", options=set(), default=True)
    bpy.types.Scene.save_blender_file = bpy.props.BoolProperty(name="Save Blender File", options=set(), default=False)
    bpy.types.Scene.save_file_name = bpy.props.StringProperty(name="Save File Name", subtype="NONE", options=set())
    bpy.types.Scene.remap_relative = bpy.props.BoolProperty(name="Remap Relative", options=set(), default=True)
    bpy.types.Scene.compress_save = bpy.props.BoolProperty(name="Compress Save", options=set(), default=False)

def sn_unregister_properties():
    del bpy.types.Scene.project_name
    del bpy.types.Scene.project_location
    del bpy.types.Scene.project_setup
    del bpy.types.Scene.folder_1
    del bpy.types.Scene.folder_2
    del bpy.types.Scene.folder_3
    del bpy.types.Scene.folder_4
    del bpy.types.Scene.folder_5
    del bpy.types.Scene.open_directory
    del bpy.types.Scene.save_blender_file
    del bpy.types.Scene.save_file_name
    del bpy.types.Scene.remap_relative
    del bpy.types.Scene.compress_save
