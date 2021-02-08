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
)

C = bpy.context
D = bpy.data


class custom_folder(PropertyGroup):

    Custom_Setup: StringProperty(
        name="Folder Name",
        description="Custom Setup Folder. \
Format for Adding Subfolders: Folder>>Subfolder>>Subsubfolder",
        default="")


class automatic_folder(PropertyGroup):

    Automatic_Setup: StringProperty(
        name="Folder Name",
        description="Automatic Setup Folder. \
Format for Adding Subfolders: Folder>>Subfolder>>Subsubfolder",
        default="")


class BLENDER_PROJECT_STARTER_APT_Preferences(AddonPreferences):
    bl_idname = __package__

    custom_folders: CollectionProperty(type=custom_folder)

    automatic_folders: CollectionProperty(type=automatic_folder)

    default_path: StringProperty(
        name="Default Project Location",
        subtype="DIR_PATH",
        default=p.expanduser("~")
    )

    save_folder: EnumProperty(
        name="Save to",
        items=subfolder_enum(),
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
        ic = context.scene.blender_project_starter_icons["BUILD_ICON"].icon_id

        layout.label(
            text="Blender Project Manager ",
            icon_value=ic
        )

        layout.prop(self, "default_path")
        layout.separator(factor=0.4)

        for index, folder in enumerate(self.automatic_folders):
            row = layout.row()
            split = row.split(factor=0.2)
            split.label(text="Folder {}".format(index + 1))

            split.prop(folder, "Automatic_Setup", text="")

            op = row.operator("blender_project_starter.remove_folder",
                              text="",
                              emboss=False,
                              icon="PANEL_CLOSE")
            op.index = index
            op.coming_from = "prefs"

        row = layout.row()
        split = row.split(factor=0.2)

        split.separator()
        op = split.operator("blender_project_starter.add_folder",
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
    custom_folder,
    automatic_folder,
    BLENDER_PROJECT_STARTER_APT_Preferences
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
