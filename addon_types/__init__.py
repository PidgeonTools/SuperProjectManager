import typing


class AddonPreferences():
    previous_set: str
    """The previous folder structure set, defaults to 'Default Folder Set'"""

    custom_folders: typing.List['ProjectFolderProps']

    automatic_folders: typing.List['ProjectFolderProps']

    project_paths: list  # CollectionProperty(type=FilebrowserEntry)
    active_project_path: int
    # IntProperty(
    #     name="Custom Property",
    #     get=get_active_project_path,
    #     set=set_active_project_path
    # )

    layout_tab: tuple
    # layout_tab: EnumProperty(
    #     name="UI Section",
    #     description="Display the different UI Elements of the Super Project Manager preferences.",
    #     items=[
    #         ("misc_settings", "General", "General settings of Super Project Manager."),
    #         ("folder_structure_sets", "Folder Structures",
    #          "Manage your folder structure settings."),
    #         ("updater", "Updater", "Check for updates and install them."),
    #     ],
    #     default="misc_settings")

    folder_structure_sets: str
    # folder_structure_sets: EnumProperty(
    #     name="Folder Structure Set",
    #     description="A list of all available folder sets.",
    #     items=structure_sets_enum,
    #     update=structure_sets_enum_update
    # )

    prefix_with_project_name: bool
    """Whether to use the project name as prefix for all folders,
    defaults to False"""

    auto_set_render_outputpath: bool
    """Whether to use the feature for automatically setting the Render Output path,
    defaults to False"""

    default_project_location: str
    """The default Project Location,
    defaults to p.expanduser("~")"""

    save_folder: tuple
    """Where to save the blend file."""

    preview_subfolders: bool
    """Show the compiled subfolder-strings in the preferences,
    defaults to False
    )"""


class ProjectFolderProps():

    render_outputpath: bool
    """If this folder input is used for setting the output path for your renders,
    defaults to False)"""

    folder_name: str
    """The folder name/path for a folder.
    defaults to ''"""
