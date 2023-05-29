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

import os
from os import path as p

import importlib

import unittest


SCRIPT_DIR = p.dirname(__file__)


def main():
    suite = None
    loader = unittest.TestLoader()

    for file in os.listdir(SCRIPT_DIR):
        if p.join(SCRIPT_DIR, file) == __file__:
            continue

        mod = importlib.import_module(p.basename(file).replace(".py", ""))
        if suite == None:
            suite = loader.loadTestsFromModule(mod)
            continue

        suite.addTests(loader.loadTestsFromModule(mod))

    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()
