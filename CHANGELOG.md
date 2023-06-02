# Changelog

## Version 1.3.1 - 2021-06-29
### Other changes
- Codestyle: Rename Addon to Super Project Manager, adjust class names

---

## Version 1.3.0 - 2021-06-27
### Features
- Feature: Automatically Set Render Output Path
- Feature: Folder Structure Sets [#14](https://github.com/PidgeonTools/SuperProjectManager/issues/14)
- Feature: Hidden Project info file, as a base for these features:
- - Open .blend file with one click
- Feature: Update BPS.json to work with the new features.

### Fixes
- Fix: Open Finder ([#16](https://github.com/PidgeonTools/SuperProjectManager/issues/16))

### Other changes
- Improvement: Better icons
- Improvement: Multiple subfolders in one Folder (Syntax: Folder>>((Subfolder1>>Subsubfolder))++Subfolder2)
- Improvement: Project display:
- - Display the number of unfinished projects (You've got n unfinished projects)
- - Option to rearrange Projects
- - Option to Sort Project in Categories
- Improvement: Update subfolder enum without restart

---

## Version 1.2.0 - 2021-02-10
### Features
- Feature: Add option to prefix folders with the project name.
- Feature: Copy file to project/target folder, even if it already exists in another folder (Inform the user):
    - Copy File Option
    - Cut File Option
    - Get File name
    - New Name Option
- Feature: Let the user decide, how many folders are in the Project Root Folder.
- Feature: Mark Project as open/unfinished

### Fixes
- Fix: Bring back property "Open Folder after Build"
- Fix: Correct Version Numbers
- Fix: Error when trying to build without specifying any Folders within the Root Folder
- Fix: Error when trying to save to subfolder
- Fix: Project Folder doesn't open on Linux
- Fix: Subfolders aren't created on Linux

### Other changes
- Codestyle: Enhance Codestyle
- Codestyle: Rename Addon to Blender Project Manager, adjust class names
- Updater: Restrict Minimal Version to 1.0.2 (Rename of branch)
- Updater: Update Addon Updater to latest version

---

## Version 1.1.0 - 2021-02-02
### Features
- Feature: Add Addon Updater for Easy Updating
- Feature: Blender file can now be saved to one of the subfolders
- Feature: Blender File Saving has been optimized and is now enabled by default
- Feature: Default File Path can now be edited from the addons preferences
- Feature: Version Counting has been implemented

### Fixes
- Fix: Clarify, what the properties mean
- Fix: Default File Path is now the Users Home-Directory
- Fix: Enable Blender 2.83 support
- Fix: File name field is only shown if the file isn't saved to any directory
- Fix: File Path Layout for Subfolder-Paths is now Folder>>Subfolder>>Subsubfolder
- Fix: Remove Social Media Buttons, add wiki and issue page instead

### Other Changes
- Code style: Split up files and make the files easy to read
