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
    "author": "Steven Scott ",
    "version": (1, 0, 0),
    "blender": (2, 91, 0),
    "location": "Scene Properties ",
    "warning": "",
    "wiki_url": "https://www.youtube.com/channel/UCiy-QcXrvu9hhe4arymNcfw",
    "tracker_url": "https://github.com/BlenderDefender/blender_project_starter/issues",
    "category": "3D View"
}


###############   IMPORTS
import bpy
from bpy.utils import previews
import os
import math

from .functions.main_functions import (
    sn_print,
    sn_cast_string,
    sn_cast_list,
    sn_cast_int_vector,
    sn_cast_int,
    sn_cast_float_vector,
    sn_cast_float,
    sn_cast_color,
    sn_cast_boolean_vector,
    sn_cast_boolean,
    sn_cast_blend_data,
    build_folder
)


###############   IMPERATIVE CODE
#######   Blender Project Starter
def sn_handle_script_line_exception(exc, line):
    print("# # # # # # # # SCRIPT LINE ERROR # # # # # # # #")
    print("Line:", line)
    raise exc


###############   EVALUATED CODE
#######   Blender Project Starter
class SNA_PT_Blender_Starter_Project_9A326(bpy.types.Panel):
    bl_label = "Blender Starter Project"
    bl_idname = "SNA_PT_Blender_Starter_Project_9A326"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'
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
            layout.prop(bpy.context.scene,"project_name",icon_value=0,text=r"Project Name",emboss=True,)
            layout.prop(bpy.context.scene,"project_location",icon_value=0,text=r"Project Location",emboss=True,)
            layout.prop(bpy.context.scene,"project_setup",icon_value=0,text=r"Project Setup",emboss=True,expand=False,)
            if r"Automatic Setup" == bpy.context.scene.project_setup:
                pass
            else:
                layout.label(text=r"Custom Folder Setup",icon_value=689)
                layout.prop(bpy.context.scene,"folder_1",icon_value=0,text=r"Folder",emboss=True,)
                layout.prop(bpy.context.scene,"folder_2",icon_value=0,text=r"Folder 2",emboss=True,)
                layout.prop(bpy.context.scene,"folder_3",icon_value=0,text=r"Folder_3",emboss=True,)
                layout.prop(bpy.context.scene,"folder_4",icon_value=0,text=r"Folder_4",emboss=True,)
                layout.prop(bpy.context.scene,"folder_5",icon_value=0,text=r"Folder_5",emboss=True,)
            layout.separator(factor=1.0)
            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            box.label(text=r".Blend Save Options",icon_value=70)
            layout.prop(bpy.context.scene,"open_directory",icon_value=0,text=r"Open Folder Window On Build",emboss=True,toggle=False,invert_checkbox=False,)
            layout.prop(bpy.context.scene,"save_blender_file",icon_value=0,text=r"Save .Blend with version number _V001",emboss=True,toggle=False,invert_checkbox=False,)
            if bpy.context.scene.save_blender_file:
                layout.prop(bpy.context.scene,"save_file_name",icon_value=0,text=r"Save File Name",emboss=True,)
                row = layout.row(align=False)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.prop(bpy.context.scene,"remap_relative",icon_value=2,text=r"Remap Relative",emboss=True,toggle=False,invert_checkbox=False,)
                row.prop(bpy.context.scene,"compress_save",icon_value=70,text=r"Compress File",emboss=True,toggle=False,invert_checkbox=False,)
            else:
                pass
            row = layout.row(align=False)
            row.enabled = True
            row.alert = False
            row.scale_x = 2.0
            row.scale_y = 2.0
            op = row.operator("sna.build_project",text=r"BUILD PROJECT",emboss=True,depress=False,icon_value=bpy.context.scene.blender_project_starter_icons['BUILD_ICON'].icon_id)
        except Exception as exc:
            print(str(exc) + " | Error in Blender Starter Project panel")


class SNA_AddonPreferences_B0705(bpy.types.AddonPreferences):
    bl_idname = __name__.partition('.')[0]
    folder_save1 : bpy.props.StringProperty(name='Folder_Save1',description='',subtype='DIR_PATH',options=set(),default='Folder//Sub')
    folder_save2 : bpy.props.StringProperty(name='Folder_Save2',description='',subtype='DIR_PATH',options=set(),default='')
    folder_save3 : bpy.props.StringProperty(name='Folder_Save3',description='',subtype='DIR_PATH',options=set(),default='')
    folder_save4 : bpy.props.StringProperty(name='Folder_Save4',description='',subtype='DIR_PATH',options=set(),default='')
    folder_save5 : bpy.props.StringProperty(name='Folder_Save5',description='',subtype='DIR_PATH',options=set(),default='')

    def draw(self, context):
        try:
            layout = self.layout
            layout.label(text=r"Blender Project Manager ",icon_value=bpy.context.scene.blender_project_starter_icons['BUILD_ICON'].icon_id)

            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            box.label(text=r"Blender Project manager ",icon_value=0)
            box.label(text=r"Here you can setup the automatic project folders ",icon_value=0)
            box.label(text=r"If you would like to add subfolders -please use double backslash Folder\\Subfolder",icon_value=2)

            layout.prop(self,"folder_save1",icon_value=0,text=r"Folder Name",emboss=True,)
            layout.prop(self,"folder_save2",icon_value=0,text=r"Folder Name 2",emboss=True,)
            layout.prop(self,"folder_save3",icon_value=0,text=r"Folder Name 3",emboss=True,)
            layout.prop(self,"folder_save4",icon_value=0,text=r"Folder Name 4 ",emboss=True,)
            layout.prop(context.preferences.addons[__name__.partition('.')[0]].preferences,"folder_save5",icon_value=0,text=r"Folder Name 5 ",emboss=True,)
            layout.separator(factor=1.0)


        except Exception as exc:
            print(str(exc) + " | Error in  addon preferences")


class SNA_OT_Build_Project(bpy.types.Operator):
    bl_idname = "sna.build_project"
    bl_label = "Build Project"
    bl_description = "Build Project Operator "
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            if r"Automatic Setup" == bpy.context.scene.project_setup:
                if True:
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save1 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save1 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save2):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save2 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save2 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save3):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save3 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save3 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save4):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save4 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save4 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save5):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save5 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + context.preferences.addons[__name__.partition('.')[0]].preferences.folder_save5 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
            else:
                if True:
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_1 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_1 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(bpy.context.scene.folder_2):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_2 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_2 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(bpy.context.scene.folder_3):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_3 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_3 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(bpy.context.scene.folder_4):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_4 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_4 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
                if sn_cast_boolean(bpy.context.scene.folder_5):
                    try: exec((r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_5 + r"'"))
                    except Exception as exc: sn_handle_script_line_exception(exc, (r"path ='" + bpy.path.abspath(os.path.join(bpy.path.abspath(bpy.context.scene.project_location),bpy.context.scene.project_name)) + r"/" + bpy.context.scene.folder_5 + r"'"))
                    try: exec(r"os.makedirs(path)")
                    except Exception as exc: sn_handle_script_line_exception(exc, r"os.makedirs(path)")
                else:
                    pass
            if bpy.context.scene.save_blender_file:
                bpy.ops.wm.save_as_mainfile(filepath=(os.path.join(bpy.path.abspath(os.path.join(bpy.context.scene.project_location,bpy.context.scene.project_name)),bpy.context.scene.save_file_name) + r"_v001.blend"),hide_props_region=True,check_existing=True,filter_blender=True,filter_backup=False,filter_image=False,filter_movie=False,filter_python=False,filter_font=False,filter_sound=False,filter_text=False,filter_archive=False,filter_btx=True,filter_collada=False,filter_alembic=False,filter_usd=False,filter_volume=False,filter_folder=True,filter_blenlib=False,filemode=8,display_type=r"DEFAULT",sort_method=r"FILE_SORT_ALPHA",compress=bpy.context.scene.compress_save,relative_remap=bpy.context.scene.remap_relative,copy=False,)
            else:
                pass
            if bpy.context.scene.open_directory:
                pass
            else:
                pass
            try: exec((r"OpenLocation =  '" + bpy.path.abspath(os.path.join(bpy.context.scene.project_location,bpy.context.scene.project_name)) + r"'"))
            except Exception as exc: sn_handle_script_line_exception(exc, (r"OpenLocation =  '" + bpy.path.abspath(os.path.join(bpy.context.scene.project_location,bpy.context.scene.project_name)) + r"'"))
            try: exec(r"OpenLocation = os.path.realpath(OpenLocation)")
            except Exception as exc: sn_handle_script_line_exception(exc, r"OpenLocation = os.path.realpath(OpenLocation)")
            try: exec(r"os.startfile(OpenLocation)")
            except Exception as exc: sn_handle_script_line_exception(exc, r"os.startfile(OpenLocation)")
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Build Project")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Build Project")
        return self.execute(context)


###############   REGISTER ICONS
def sn_register_icons():
    icons = ["BUILD_ICON","TWITTER","YOUTUBE","GUMROAD",]
    bpy.types.Scene.blender_project_starter_icons = bpy.utils.previews.new()
    icons_dir = os.path.join( os.path.dirname( __file__ ), "icons" )
    for icon in icons:
        bpy.types.Scene.blender_project_starter_icons.load( icon, os.path.join( icons_dir, icon + ".png" ), 'IMAGE' )

def sn_unregister_icons():
    bpy.utils.previews.remove( bpy.types.Scene.blender_project_starter_icons )


###############   REGISTER PROPERTIES
def sn_register_properties():
    bpy.types.Scene.project_name = bpy.props.StringProperty(name='Project Name',description='',subtype='NONE',options=set(),default='My_Project')
    bpy.types.Scene.project_location = bpy.props.StringProperty(name='Project Location',description='Saves the location of file',subtype='DIR_PATH',options=set(),default='C:\Blender_External')
    bpy.types.Scene.project_setup = bpy.props.EnumProperty(name='Project Setup',description='',options=set(),items=[('Automatic Setup', 'Automatic Setup', 'Automatic Project Setup '), ('Custom Setup', 'Custom Setup', 'My Custom Setup')])
    bpy.types.Scene.folder_1 = bpy.props.StringProperty(name='Folder_1',description='Custom Folder Setup',subtype='DIR_PATH',options=set(),default='')
    bpy.types.Scene.folder_2 = bpy.props.StringProperty(name='Folder_2',description='Folder Structure 2 ',subtype='DIR_PATH',options=set(),default='')
    bpy.types.Scene.folder_3 = bpy.props.StringProperty(name='Folder_3',description='Custom Folder 3 ',subtype='DIR_PATH',options=set(),default='')
    bpy.types.Scene.folder_4 = bpy.props.StringProperty(name='Folder_4',description='Custom Folder 4',subtype='DIR_PATH',options=set(),default='')
    bpy.types.Scene.folder_5 = bpy.props.StringProperty(name='Folder_5',description='Custom Folder 5',subtype='DIR_PATH',options=set(),default='')
    bpy.types.Scene.open_directory = bpy.props.BoolProperty(name='Open Directory',description='',options=set(),default=True)
    bpy.types.Scene.save_blender_file = bpy.props.BoolProperty(name='Save Blender File',description='',options=set(),default=False)
    bpy.types.Scene.save_file_name = bpy.props.StringProperty(name='Save File Name',description='',subtype='NONE',options=set(),default='')
    bpy.types.Scene.remap_relative = bpy.props.BoolProperty(name='Remap Relative',description='',options=set(),default=True)
    bpy.types.Scene.compress_save = bpy.props.BoolProperty(name='Compress Save',description='',options=set(),default=False)

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


###############   REGISTER ADDON
def register():
    sn_register_icons()
    sn_register_properties()
    bpy.utils.register_class(SNA_PT_Blender_Starter_Project_9A326)
    bpy.utils.register_class(SNA_AddonPreferences_B0705)
    bpy.utils.register_class(SNA_OT_Build_Project)


###############   UNREGISTER ADDON
def unregister():
    sn_unregister_icons()
    sn_unregister_properties()
    bpy.utils.unregister_class(SNA_OT_Build_Project)
    bpy.utils.unregister_class(SNA_AddonPreferences_B0705)
    bpy.utils.unregister_class(SNA_PT_Blender_Starter_Project_9A326)