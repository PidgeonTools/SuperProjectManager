# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Blender Project Starter is made for automatic Project Folder Generation.>
#    Copyright (C) <2021>  <Steven Scott>
#    Modified <2021> <Blender Defender>
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


import os
from os import path as p
import shutil

from .functions.register_functions import (
    register_icons,
    register_properties,
    unregister_icons,
)

from .functions.blenderdefender_functions import (
    setup_addons_data,
    update_json
)

from . import (
    operators,
    prefs,
    panels
)

bl_info = {
    "name": "Super Project Manager (SPM)",
    "description": "Manage and setup your projects the easy way!",
    "author": "Blender Defender",
    "version": (1, 3, 1),
    "blender": (2, 83, 0),
    "location": "Properties >> Scene Properties >> Super Project Manager",
    "warning": "",
    "wiki_url": "https://github.com/BlenderDefender/blender_project_manager/wiki",
    "tracker_url": "https://github.com/BlenderDefender/\
blender_project_manager/issues",
    "category": "System"
}


def register():
    path = p.join(p.expanduser("~"),
                  "Blender Addons Data",
                  "blender-project-starter")

    setup_addons_data()
    if "BPS.json" not in os.listdir(path):
        shutil.copyfile(p.join(p.dirname(__file__),
                               "functions",
                               "BPS.json"),
                        p.join(path, "BPS.json"))

    update_json()

    prefs.register(bl_info)
    operators.register()
    panels.register()

    register_icons()
    register_properties()


def unregister():
    operators.unregister()
    prefs.unregister()
    panels.unregister()

    unregister_icons()
