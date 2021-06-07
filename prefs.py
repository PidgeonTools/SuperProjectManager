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
    EnumProperty,
    CollectionProperty,
    BoolProperty,
    IntProperty
)
from bpy.types import (
    PropertyGroup,
    AddonPreferences
)

import os
from os import path as p

from . import addon_updater_ops

from .functions.main_functions import (
    subfolder_enum,
    structure_sets_enum,
    structure_sets_enum_update
)

C = bpy.context
D = bpy.data


class project_folder_props(PropertyGroup):

    render_outputpath = BoolProperty(
        name="Render Output",
        description="Output path for your renders.",
        default=False)
    folder_name = StringProperty(
        name="Folder Name",
        description="Automatic Setup Folder. \
Format for Adding Subfolders: Folder>>Subfolder>>Subsubfolder",
        default="")


class BLENDER_PROJECT_MANAGER_APT_Preferences(AddonPreferences):
    bl_idname = __package__
    previous_set: StringProperty(default="Default Folder Set")

    custom_folders: CollectionProperty(type=project_folder_props)

    automatic_folders: CollectionProperty(type=project_folder_props)

    folder_structure_sets = EnumProperty(
        name="Folder Structure Set",
        description="A list of all available folder sets.",
        items=structure_sets_enum,
        update=structure_sets_enum_update
    )

    prefix_with_project_name = BoolProperty(
        name="Project Name Prefix",
        description="If enabled, use the project name as prefix for all folders.",
        default=False,
    )

    auto_set_render_outputpath = BoolProperty(
        name="Auto Set Render Output Path",
        description="If enabled, the Auto Set render Output path feature can be used.",
        default=False,
    )

    default_path: StringProperty(
        name="Default Project Location",
        subtype="DIR_PATH",
        default=p.expanduser("~")
    )

    save_folder: EnumProperty(
        name="Save to",
        items=subfolder_enum
    )

    auto_check_update = BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months = IntProperty(
        name="Months",
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = IntProperty(
        name="Days",
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = IntProperty(
        name="Hours",
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = IntProperty(
        name="Minutes",
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        layout = self.layout
        ic = context.scene.blender_project_manager_icons["BUILD_ICON"].icon_id

        layout.label(
            text="Blender Project Manager ",
            icon_value=ic
        )

        layout.prop(self, "prefix_with_project_name")
        layout.prop(self, "auto_set_render_outputpath")
        layout.prop(self, "default_path")
        layout.separator(factor=0.4)

        render_outpath_active = True in [
            e.render_outputpath for e in self.automatic_folders]

        row = layout.row(align=True)
        row.prop(self, "folder_structure_sets")
        row.operator("blender_project_manager.add_structure_set",
                     text="", icon="ADD")
        op = row.operator(
            "blender_project_manager.remove_structure_set", text="", icon="REMOVE")
        op.structure_set = self.previous_set
        for index, folder in enumerate(self.automatic_folders):
            row = layout.row()
            split = row.split(factor=0.2)
            split.label(text="Folder {}".format(index + 1))

            if self.auto_set_render_outputpath:
                col = split.column()
                col.enabled = folder.render_outputpath or not render_outpath_active
                col.prop(folder, "render_outputpath")
            split.prop(folder, "folder_name", text="")

            op = row.operator("blender_project_manager.remove_folder",
                              text="",
                              emboss=False,
                              icon="PANEL_CLOSE")
            op.index = index
            op.coming_from = "prefs"

        row = layout.row()
        split = row.split(factor=0.2)

        split.separator()
        op = split.operator("blender_project_manager.add_folder",
                            icon="PLUS")
        op.coming_from = "prefs"

        mainrow = layout.row()
        col = mainrow.column()

        # updater draw function
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        # 1) check for update/update now buttons
        # 2) toggle for auto-check(interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column,
        # to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # col.operator("wm.url_open","Open webpage ").url=\
        # addon_updater_ops.updater.website


classes = (
    project_folder_props,
    BLENDER_PROJECT_MANAGER_APT_Preferences
)


def register(bl_info):
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)

    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # avoid blender 2.8 warnings
        bpy.utils.register_class(cls)


def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
