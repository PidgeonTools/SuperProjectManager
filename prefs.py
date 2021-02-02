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

from . import addon_updater_ops


class BLENDER_PROJECT_STARTER_APT_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    default_path: bpy.props.StringProperty(
        name="Default Project Location",
        subtype="DIR_PATH",
        default=p.expanduser("~")
    )
    folder_1: bpy.props.StringProperty(
        name="Folder Name 1",
        default="Blender Files"
    )
    folder_2: bpy.props.StringProperty(
        name="Folder Name 2",
        default="Textures"
    )
    folder_3: bpy.props.StringProperty(
        name="Folder Name 3",
        default="Rendered Images"
    )
    folder_4: bpy.props.StringProperty(
        name="Folder Name 4",
        default="References"
    )
    folder_5: bpy.props.StringProperty(
        name="Folder Name 5",
        default="Sounds"
    )

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context):
        layout = self.layout

        layout.label(
            text="Blender Project Manager ",
            icon_value=bpy.context.scene.blender_project_starter_icons["BUILD_ICON"].icon_id
        )

        box = layout.box()
        box.enabled = True
        box.alert = False
        box.scale_x = 1.0
        box.scale_y = 1.0
        box.label(text="Blender Project manager ", icon_value=0)
        box.label(text="Here you can setup the automatic project folders ", icon_value=0)
        box.label(text="Format for adding subfolders: Folder>>Subfolder>>Subsubfolder")

        layout.prop(self, "default_path")
        layout.prop(self, "folder_1")
        layout.prop(self, "folder_2")
        layout.prop(self, "folder_3")
        layout.prop(self, "folder_4")
        layout.prop(self, "folder_5")

        layout = self.layout
        # col = layout.column() # works best if a column, or even just self.layout
        mainrow = layout.row()
        col = mainrow.column()

        # updater draw function
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # col.operator("wm.url_open","Open webpage ").url=addon_updater_ops.updater.website


classes = (
    BLENDER_PROJECT_STARTER_APT_Preferences,
)


def register(bl_info):
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)

    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)


def unregister():
    # addon updater unregister
    addon_updater_ops.unregister()

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
