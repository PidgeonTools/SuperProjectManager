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

import re

from .operators import (
    SUPER_PROJECT_MANAGER_OT_add_folder,
    SUPER_PROJECT_MANAGER_OT_remove_folder,
    SUPER_PROJECT_MANAGER_OT_add_collection,
    SUPER_PROJECT_MANAGER_OT_remove_collection,
    SUPER_PROJECT_MANAGER_ot_add_structure_set,
    SUPER_PROJECT_MANAGER_ot_remove_structure_set
)

from . import addon_updater_ops

from .functions.main_functions import (
    structure_sets_enum,
    structure_sets_enum_update,
    active_project_enum,
    active_project_enum_update
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


class project_collection_props(PropertyGroup):
    color: EnumProperty(
        name="Color",
        description="",
        items=[
            ("NONE", "No Color", "", "OUTLINER_COLLECTION", 0),
            ("COLOR_01", "Color 1", "", "COLLECTION_COLOR_01", 1),
            ("COLOR_02", "Color 2", "", "COLLECTION_COLOR_02", 2),
            ("COLOR_03", "Color 3", "", "COLLECTION_COLOR_03", 3),
            ("COLOR_04", "Color 4", "", "COLLECTION_COLOR_04", 4),
            ("COLOR_05", "Color 5", "", "COLLECTION_COLOR_05", 5),
            ("COLOR_06", "Color 6", "", "COLLECTION_COLOR_06", 6),
            ("COLOR_07", "Color 7", "", "COLLECTION_COLOR_07", 7),
            ("COLOR_08", "Color 8", "", "COLLECTION_COLOR_08", 8)
        ],
        default="NONE")

    collection_name: StringProperty(
        name="Collection Name",
        description="Automatic Setup Collection",
        default="")


class FilebrowserEntry(PropertyGroup):

    icon: StringProperty(default="FILE_FOLDER")
    is_valid: BoolProperty()
    """Whether this path is currently reachable"""

    name: StringProperty()

    path: StringProperty()

    use_save: BoolProperty()
    """Whether this path is saved in bookmarks, or generated from OS"""


def get_active_project_path(self):
    active_directory = bpy.context.space_data.params.directory.decode(
        encoding="utf-8")

    for i, p in enumerate(self.project_paths):
        if os.path.normpath(p.path) == os.path.normpath(active_directory):
            return i

    return -1


def set_active_project_path(self, value):
    bpy.context.space_data.params.directory = self.project_paths[value].path.encode(
    )

    # Custom setter logic
    self["active_project_path"] = value


class SUPER_PROJECT_MANAGER_APT_Preferences(AddonPreferences):
    bl_idname = __package__
    previous_set: StringProperty(default="Default Folder Set")

    custom_folders: CollectionProperty(type=project_folder_props)

    automatic_folders: CollectionProperty(type=project_folder_props)
    automatic_collections: CollectionProperty(type=project_collection_props)

    active_project: EnumProperty(
        name="Active Project",
        description="Which project should be displayed in the Filebrowser panel.",
        items=active_project_enum,
        update=active_project_enum_update
    )

    project_paths: CollectionProperty(type=FilebrowserEntry)
    active_project_path: IntProperty(
        name="Custom Property",
        get=get_active_project_path,
        set=set_active_project_path
    )

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

    enable_additional_rearrange_tools: BoolProperty(
        name="Enable additional rearrange operators",
        description="Enable the 'Move to top' and 'Move to bottom' operator. This will make the rearrange panel more crowded",
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

        # Display warning, if a backup of a corrupted file is in the Addons Data directory
        addons_data_dir = p.join(p.expanduser(
            "~"), "Blender Addons Data", "blender-project-starter")
        corrupted_files = [file for file in os.listdir(
            addons_data_dir) if re.match("BPS\.\d\d\d\d-\d\d-\d\d\.json", file)]
        if len(corrupted_files) > 0:
            layout.separator()

            box = layout.box()
            box.label(
                text="Warning: Corrupted Addon Data files detected", icon="ERROR")
            box.label(
                text="Click 'Open directory' below to view the corrupted files or click 'Support' for help on Discord.")
            box.label(text="Corrupted files:")
            for f in corrupted_files:
                row = box.row()
                row.scale_y = 0.4
                row.label(text=f)

            box.operator(
                "wm.path_open", text="Open directory").filepath = addons_data_dir

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
        layout.separator(factor=0.4)

        layout.prop(self, "enable_additional_rearrange_tools")

    def draw_folder_structure_sets(self, context: Context, layout: UILayout):
        layout.label(text="Folder Structure Set")

        row = layout.row(align=True)
        row.prop(self, "folder_structure_sets", text="")
        row.operator(SUPER_PROJECT_MANAGER_ot_add_structure_set.bl_idname,
                     text="", icon="ADD")
        op = row.operator(
            SUPER_PROJECT_MANAGER_ot_remove_structure_set.bl_idname, text="", icon="REMOVE")
        op.structure_set = self.previous_set

        # Layout the Box containing the folder structure properties.
        box = layout.box()
        box.separator(factor=FOLDER_BOX_PADDING_Y)

        compiled_preview_string = ""
        for index, folder in enumerate(self.automatic_folders):
            self.draw_folder_props(index, folder, box)
            compiled_preview_string += "((" + folder.folder_name + "))++"

        # Add folder button
        box.separator(factor=ADD_FOLDER_BUTTON_MARGIN_TOP)

        row = box.row()
        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding left

        op = row.operator(SUPER_PROJECT_MANAGER_OT_add_folder.bl_idname,
                          icon="PLUS")
        op.coming_from = "prefs"
        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding right

        box.separator(factor=FOLDER_BOX_PADDING_Y)  # Padding bottom

        # Expand/Collapse Preview of compiled subfolders
        row = box.row()
        row.alignment = "LEFT"
        icon = "TRIA_DOWN" if self.preview_subfolders else "TRIA_RIGHT"
        row.prop(self, "preview_subfolders",
                 emboss=False, icon=icon, text="Preview")

        # Preview complete folder structure
        if self.preview_subfolders:

            prefix = ""
            if self.prefix_with_project_name:
                prefix = "Project_Name_"

            for line in str(Subfolders(compiled_preview_string, prefix)).split("\n"):
                row = box.row()
                row.split(factor=FOLDER_BOX_PADDING_X)
                row.scale_y = 0.3
                row.label(text=line)

        layout.label(text="Automatic Collections")

        box = layout.box()
        for index, collection in enumerate(self.automatic_collections):
            collection: 'project_collection_props'

            row = box.row()
            row.split(factor=FOLDER_BOX_PADDING_X)  # Padding left

            # Collection Color
            row.prop(collection, "color", icon_only=True,
                     emboss=False, text="")

            # Collection name
            row.prop(collection, "collection_name", text="")

            # Remove button
            op = row.operator(SUPER_PROJECT_MANAGER_OT_remove_collection.bl_idname,
                              text="",
                              emboss=False,
                              icon="PANEL_CLOSE")
            op.index = index

            row.split(factor=FOLDER_BOX_PADDING_X)  # Padding right

        row = box.row()

        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding left
        row.operator(
            SUPER_PROJECT_MANAGER_OT_add_collection.bl_idname, text="Add Collection", icon="PLUS")
        row.split(factor=FOLDER_BOX_PADDING_X)  # Padding right

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
        op = row.operator(SUPER_PROJECT_MANAGER_OT_remove_folder.bl_idname,
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
    project_collection_props,
    FilebrowserEntry,
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
