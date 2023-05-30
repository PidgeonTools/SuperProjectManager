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
    from objects.path_generator import Subfolders, Token


class TestSubfolders(unittest.TestCase):
    def test_compile_paths(self):
        # Test a simple folder path with subfolders. Shouldn't result in a warning.
        test_case = Subfolders("Folder>>Subfolder>>Subsubfolder")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder\\Subsubfolder"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test a simple folder path with a prefix. Shouldn't result in a warning.
        test_case = Subfolders(
            "Folder>>Subfolder>>Subsubfolder", "Test_Prefix_")
        self.assertEqual(test_case.compile_paths(), [
            "Test_Prefix_Folder",
            "Test_Prefix_Folder\\Test_Prefix_Subfolder",
            "Test_Prefix_Folder\\Test_Prefix_Subfolder\\Test_Prefix_Subsubfolder"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test a folder path with multiple subfolders in a Folder.
        # Shouldn't result in a warning.
        test_case = Subfolders(
            "Folder>>Subfolder1++Subfolder2>>Subsubfolder")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder\\Subfolder1",
            "Folder\\Subfolder2",
            "Folder\\Subfolder2\\Subsubfolder"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test a simple folder path with subfolders and '++' following '>>'.
        # Shouldn't result in a warning, because '>>' is preferred over '++'.
        test_case = Subfolders("Folder>>Subfolder1>>++Subfolder2")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder\\Subfolder1",
            "Folder\\Subfolder1\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test a simple folder path with subfolders and '>>' following '++'.
        # Shouldn't result in a warning, because '>>' is preferred over '++'.
        test_case = Subfolders("Folder++Folder2++>>Test>>Amazing")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder2",
            "Folder2\\Test",
            "Folder2\\Test\\Amazing"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test a simple folder path that ends with '>>'. Should result in a warning.
        test_case = Subfolders(
            "Folder>>Subfolder1++Subfolder2>>")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder\\Subfolder1",
            "Folder\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [
            "A folder path should not end with '>>'!"
        ])

        # Test a folder path with brackets. Shouldn't result in a warning.
        test_case = Subfolders(
            "Folder>>Subfolder++((Subfolder2>>Subsubfolder))++Subfolder3")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder2",
            "Folder\\Subfolder2\\Subsubfolder",
            "Folder\\Subfolder3"
        ])
        self.assertEqual(test_case.warnings, [])

        # Test a folder path with unmatched brackets and a misplaced '>>'.
        # Should result in two warnings.
        test_case = Subfolders(
            "Folder((>>Subfolder>>Subsubfolder1++Subfolder2")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Subfolder",
            "Subfolder\\Subsubfolder1",
            "Subfolder\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [
            "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!",
            "A '>>' can't be used until at least one Folder name is specified! This rule also applies for subfolders.",
        ])

        # Test a folder path with unmatched opening brackets.
        # Should result in a warning.
        test_case = Subfolders(
            "Folder((++Subfolder>>Subsubfolder1++Subfolder2")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Subfolder",
            "Subfolder\\Subsubfolder1",
            "Subfolder\\Subfolder2"
        ])
        self.assertEqual(test_case.warnings, [
            "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!"
        ])

        # Test a folder path with unmatched closing brackets.
        # Should result in a warning.
        test_case = Subfolders(
            "Folder>>Subfolder>>Subsubfolder1))++Subfolder2")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder\\Subsubfolder1"
        ])
        self.assertEqual(test_case.warnings, [
            "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!"
        ])

        # Test a folder path with brackets and a misplaced '>>'.
        # Should result in a warning.
        test_case = Subfolders(
            "((Folder>>Subfolder++Subfolder2))>>Subsubfolder1++Subsubfolder2")
        self.assertEqual(test_case.compile_paths(), [
            "Folder",
            "Folder\\Subfolder",
            "Folder\\Subfolder2",
            "Subsubfolder1",
            "Subsubfolder2"
        ])
        self.assertEqual(test_case.warnings, [
                         "A '>>' can't be used until at least one Folder name is specified! This rule also applies for subfolders."])

    def test_tokenize(self):
        test_obj = Subfolders("Placeholder")
        self.assertEqual(test_obj.tokenize("Test"), [Token("Test")])
        self.assertEqual(test_obj.tokenize("Test>>++((Test)))"), [Token("Test"), Token(
            ">"), Token("+"), Token("("), Token("Test"), Token(")"), Token(")")])


def main():
    unittest.main()


if __name__ == "__main__":
    main()
