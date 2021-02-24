[![Donate](https://img.shields.io/badge/DONATE!%20Funding%20Goal%3A%20%241000%20(1%20Week%20Developer%20Time)-%2430-red?style=for-the-badge&logo=paypal)](https://www.paypal.com/donate?hosted_button_id=DZE9NFSFPFMYS)  
![GitHub](https://img.shields.io/github/license/BlenderDefender/blender_project_starter?color=green&style=for-the-badge)
[![GitHub issues](https://img.shields.io/github/issues/BlenderDefender/blender_project_starter?style=for-the-badge)](https://github.com/BlenderDefender/blender_pm/issues)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BlenderDefender/blender_project_starter?style=for-the-badge)
# Blender PM (Project Manager)

## Upcoming Version:
- [x] Fix: Open Finder ([Issue #16](https://github.com/BlenderDefender/blender_pm/issues/16))
- [ ] Improvement: Better icons
- [ ] Improvement: Update subfolder enum without restart
- [ ] Feature: Open .blend file with one click
- [ ] Feature: Folder Structure Sets [#14](https://github.com/BlenderDefender/blender_project_manager/issues/14)



<!--
We've just hit another update. No features are planned so far. [Change this!](https://github.com/BlenderDefender/blender_project_manager/issues)
-->

## Changelog:

Version 1.2.0
* Fix: Project Folder doesn't open on Linux
* Fix: Subfolders aren't created on Linux
* Fix: Bring back property "Open Folder after Build"
* Fix: Error when trying to build without specifying any Folders within the Root Folder
* Fix: Error when trying to save to subfolder
* Fix: Correct Version Numbers
* Codestyle: Enhance Codestyle
* Codestyle: Rename Addon to Blender Project Manager, adjust class names
* Feature: Mark Project as open/unfinished
* Feature: Add option to prefix folders with the project name.
* Feature: Let the user decide, how many folders are in the Project Root Folder.
* Feature: Copy file to project/target folder, even if it already exists in another folder (Inform the user):
    * Get File name
    * Cut File Option
    * Copy File Option
    * New Name Option
* Updater: Update Addon Updater to latest version
* Updater: Restrict Minimal Version to 1.0.2 (Rename of branch)

Version 1.1.0:
* Feature: Add Addon Updater for Easy Updating
* Fix: Enable Blender 2.83 support
* Fix: Remove Social Media Buttons, add wiki and issue page instead
* Code style: Split up files and make the files easy to read
* Fix: File Path Layout for Subfolder-Paths is now Folder>>Subfolder>>Subsubfolder
* Fix: Default File Path is now the Users Home-Directory
* Feature: Default File Path can now be edited from the addons preferences
* Fix: Clarify, what the properties mean
* Feature: Blender File Saving has been optimized and is now enabled by default
* Feature: Version Counting has been implemented
* Feature: Blender file can now be saved to one of the subfolders
* Fix: File name field is only shown if the file isn't saved to any directory

## System requirements:
| **OS** | **Blender** |
| ------------- | ------------- |
| OSX | Testing, please give feedback if it works for you. |
| Windows | Blender 2.83+ |
| Linux | Blender 2.83+ |
