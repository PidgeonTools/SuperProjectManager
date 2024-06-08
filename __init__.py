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

import os
from os import path as p
import shutil

from .functions.register_functions import (
    register_properties,
)

from .functions.blenderdefender_functions import (
    setup_addons_data,
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
    "doc_url": "https://github.com/PidgeonTools/SuperProjectManager/wiki",
    "tracker_url": "https://github.com/PidgeonTools/SuperProjectManager/issues",
    "endpoint_url": "https://raw.githubusercontent.com/PidgeonTools/SAM-Endpoints/main/SuperProjectManager.json",
    "category": "System"
}


def register():
    setup_addons_data()

    if bpy.app.version < (4, 2):
        prefs.legacy_register(bl_info)
    else:
        prefs.register()

    operators.register()
    panels.register()

    register_properties()


def unregister():
    operators.unregister()
    prefs.unregister()
    panels.unregister()
