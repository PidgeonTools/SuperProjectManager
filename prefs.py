# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Super Project Manager helps you manage your Blender Projects.>
#    Copyright (C) <2023>  <Blender Defender>
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
    AddonPreferences,
    Context,
    UILayout
)

import os
from os import path as p

from . import addon_updater_ops

from .functions.main_functions import (
    structure_sets_enum,
    structure_sets_enum_update
)

from .objects.path_generator import (
    Subfolders,
    subfolder_enum,
)

C = bpy.context
D = bpy.data

FOLDER_BOX_PADDING_X = 0.1
FOLDER_BOX_PADDING_Y = 1
WARNING_MARGIN_BOTTOM = 0.2
ADD_FOLDER_BUTTON_MARGIN_TOP = 0.4


class project_folder_props(PropertyGroup):

    render_outputpath: BoolProperty(
        name="Render Output",
        description="Set the last path this folder input results in as output path for your renders",
        default=False)
    folder_name: StringProperty(
        name="Folder Name",
        description="Automatic Setup Folder. \
Format for Adding Subfolders: Folder>>Subfolder>>Subsubfolder",
        default="")


class SUPER_PROJECT_MANAGER_APT_Preferences(AddonPreferences):
    bl_idname = __package__
    previous_set: StringProperty(default="Default Folder Set")

    custom_folders: CollectionProperty(type=project_folder_props)

    automatic_folders: CollectionProperty(type=project_folder_props)

    layout_tab: EnumProperty(
        name="UI Section",
        description="Display the different UI Elements of the Super Project Manager preferences.",
        items=[
            ("misc_settings", "General", "General settings of Super Project Manager."),
            ("folder_structure_sets", "Folder Structures",
             "Manage your folder structure settings."),
            ("updater", "Updater", "Check for updates and install them."),
        ],
        default="misc_settings")

    folder_structure_sets: EnumProperty(
        name="Folder Structure Set",
        description="A list of all available folder sets.",
        items=structure_sets_enum,
        update=structure_sets_enum_update
    )

    prefix_with_project_name: BoolProperty(
        name="Project Name Prefix",
        description="If enabled, use the project name as prefix for all folders",
        default=False,
    )

    auto_set_render_outputpath: BoolProperty(
        name="Auto Set Render Output Path",
        description="If enabled, the feature to automatically set the Render Output path can be used",
        default=False,
    )

    default_project_location: StringProperty(
        name="Default Project Location",
        subtype="DIR_PATH",
        default=p.expanduser("~")
    )

    save_folder: EnumProperty(
        name="Save to",
        items=subfolder_enum
    )

    preview_subfolders: BoolProperty(
        name="Preview compiled Subfolders",
        description="Show the compiled subfolder-strings in the preferences",
        default=False
    )

    auto_check_update: BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )
    updater_intrval_months: IntProperty(
        name="Months",
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_intrval_days: IntProperty(
        name="Days",
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31
    )
    updater_intrval_hours: IntProperty(
        name="Hours",
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_intrval_minutes: IntProperty(
        name="Minutes",
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )

    def draw(self, context: Context):
        layout: UILayout = self.layout

        # Layout Tabs to switch between Settings Tabs.
        row = layout.row(align=True)
        row.scale_y = 1.3
        row.prop(self, "layout_tab", expand=True)

        if self.layout_tab == "misc_settings":
            self.draw_misc_settings(context, layout)

        if self.layout_tab == "folder_structure_sets":
            self.draw_folder_structure_sets(context, layout)

        if self.layout_tab == "updater":
            # updater draw function
            # could also pass in col as third arg
            addon_updater_ops.update_settings_ui(self, context)

        # Support URL
        layout.separator()
        col = layout.column()
        op = col.operator("wm.url_open", text="Support", icon="URL")
        op.url = "https://bd-links.netlify.app/discord-spm"

    def draw_misc_settings(self, context: Context, layout: UILayout):
        layout.label(text="Default Project Location")
        layout.prop(self, "default_project_location", text="")
        layout.separator(factor=0.4)

        layout.prop(self, "prefix_with_project_name",
                    text="Add the Project Name as Folder Prefix")
        layout.separator(factor=0.4)

        layout.prop(self, "auto_set_render_outputpath",
                    text="Automatically set the render output path")

    def draw_folder_structure_sets(self, context: Context, layout: UILayout):
        layout.label(text="Folder Structure Set")

        # TODO
        # row = layout.row()
        # row.prop(self, "preview_subfolders")

        row = layout.row(align=True)
        row.prop(self, "folder_structure_sets", text="")
        row.operator("super_project_manager.add_structure_set",
                     text="", icon="ADD")
        op = row.operator(
            "super_project_manager.remove_structure_set", text="", icon="REMOVE")
        op.structure_set = self.previous_set

        # Layout the Box containing the folder structure properties.
        box = layout.box()
        box.separator(factor=FOLDER_BOX_PADDING_Y)

        for index, folder in enumerate(self.automatic_folders):
            self.draw_folder_props(index, folder, box)

        # Add folder button
        box.separator(factor=ADD_FOLDER_BUTTON_MARGIN_TOP)

        row = box.row()
        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding left

        op = row.operator("super_project_manager.add_folder",
                          icon="PLUS")
        op.coming_from = "prefs"
        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding right

        box.separator(factor=FOLDER_BOX_PADDING_Y)  # Padding bottom

        # TODO: Preview complete folder structure
        if self.preview_subfolders and False:
            box = layout.box()
            for path in Subfolders(folder.folder_name).display_tree:
                row = box.row()
                row.label(text=path)

    def draw_folder_props(self, index: int, folder: 'project_folder_props', layout: UILayout):
        render_outpath_active = True in [
            e.render_outputpath for e in self.automatic_folders]

        row = layout.row()
        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding left

        # # split.label(text="Folder {}".format(index + 1))

        # Folder Name/Path Property
        row.prop(folder, "folder_name", text="")

        # Render Output Path
        if self.auto_set_render_outputpath:
            col = row.column()
            col.enabled = folder.render_outputpath or not render_outpath_active
            col.prop(folder, "render_outputpath",
                     text="", icon="OUTPUT", emboss=folder.render_outputpath)

            # Remove Icon
        op = row.operator("super_project_manager.remove_folder",
                          text="",
                          emboss=False,
                          icon="PANEL_CLOSE")
        op.index = index
        op.coming_from = "prefs"

        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding right

        for warning in Subfolders(folder.folder_name).warnings:
            row = layout.row()
            row.split(factor=FOLDER_BOX_PADDING_X)  # Padding left

            row.label(text=warning, icon="ERROR")
            layout.separator(factor=WARNING_MARGIN_BOTTOM)

            row.split(factor=FOLDER_BOX_PADDING_X)  # Padding right


classes = (
    project_folder_props,
    SUPER_PROJECT_MANAGER_APT_Preferences
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
