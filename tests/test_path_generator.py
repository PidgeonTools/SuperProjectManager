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

import unittest

from os import path as p

import sys
sys.path.append(p.dirname(p.dirname(__file__)))

if True:
    from objects.path_generator import Subfolders


class TestSubfolders(unittest.TestCase):
    def test_compile_paths(self):
        # Test Case 1
        test_case = Subfolders(
            "Folder>>Subfolder++((Subfolder2>>Subsubfolder))++Subfolder3")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder2",
            "Folder\\Subfolder2\\Subsubfolder",
            "Folder\\Subfolder3"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test Case 2
        test_case = Subfolders("Folder++Folder2++>>Test>>Amazing")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder2",
            "Folder2\\Test",
            "Folder2\\Test\\Amazing"
        ])
        self.assertEqual(test_case.warnings, [
            "A ++ can't be used until at least one Folder name is specified and one >> is used. This also applies for Brackets!",
            "A ++ can't be followed by >>"
        ])

        # Test Case 3
        test_case = Subfolders("Folder>>Subfolder>>Subsubfolder")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder\\Subsubfolder"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test Case 4
        test_case = Subfolders(
            "Folder>>Subfolder1++Subfolder2>>Subsubfolder")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder1",
            "Folder\\Subfolder2",
            "Folder\\Subfolder2\\Subsubfolder"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test Case 5
        test_case = Subfolders(
            "Folder>>((Subfolder1>>Subsubfolder1))++Subfolder2>>Subsubfolder2")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder1",
            "Folder\\Subfolder1\\Subsubfolder1",
            "Folder\\Subfolder2",
            "Folder\\Subfolder2\\Subsubfolder2"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test Case 6
        test_case = Subfolders("Folder>>Subfolder1>>++Subfolder2")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder1",
            "Folder\\Subfolder1\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, ["A >> can't be followed by ++"])

        # Test Case 7
        test_case = Subfolders(
            "Folder>>((Subfolder>>Subsubfolder1++Subfolder2")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder\\Subsubfolder1",
            "Folder\\Subfolder\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [
            "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!"
        ])

        # Test Case 8
        test_case = Subfolders(
            "Folder((>>Subfolder>>Subsubfolder1++Subfolder2")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Subfolder",
            "Subfolder\\Subsubfolder1",
            "Subfolder\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [
            "A >> can't be used until at least one Folder name is specified. This also applies for Brackets!",
            "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!"
        ])

        # Test Case 9
        test_case = Subfolders(
            "Folder((++Subfolder>>Subsubfolder1++Subfolder2")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Subfolder",
            "Subfolder\\Subsubfolder1",
            "Subfolder\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [
            "A ++ can't be used until at least one Folder name is specified and one >> is used. This also applies for Brackets!",
            "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!"
        ])

        # Test Case 10
        test_case = Subfolders(
            "Folder++Subfolder>>Subsubfolder1++Subfolder2>>")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Subfolder",
            "Subfolder\\Subsubfolder1",
            "Subfolder\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [
            "A ++ can't be used until at least one Folder name is specified and one >> is used. This also applies for Brackets!",
            "A string should end with a folder name, not with >> or ++!"
        ])

        # Test Case 11
        test_case = Subfolders(
            "Folder>>Subfolder>>Subsubfolder1))++Subfolder2")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder\\Subsubfolder1"
        ])
        self.assertEqual(test_case.warnings, [
            "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!"
        ])

        # Test Case 12
        test_case = Subfolders(
            "((Folder>>Subfolder++Subfolder2))>>Subsubfolder1++Subsubfolder2")
        self.assertEqual(test_case.paths, [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder2",
            "Folder\\Subfolder2\\Subsubfolder1",
            "Folder\\Subfolder2\\Subsubfolder2"
        ])
        self.assertEqual(test_case.warnings, [])

    def test_compile_display_paths(self):
        test_obj = Subfolders("Placeholder")

        self.assertEqual(test_obj.compile_display_paths(
            ["Folder//Subfolder//Subfolder3"]), ["Folder>>Subfolder>>Subfolder3"])

        self.assertEqual(test_obj.compile_display_paths(
            ["Folder/Subfolder/Subfolder3"]), ["Folder>>Subfolder>>Subfolder3"])

        self.assertEqual(test_obj.compile_display_paths(
            ["Folder\\Subfolder\\Subfolder3"]), ["Folder>>Subfolder>>Subfolder3"])


def main():
    unittest.main()


if __name__ == "__main__":
    main()
