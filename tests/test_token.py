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
    from objects.path_generator import Token


class TestToken(unittest.TestCase):
    def test_token_type(self):
        self.assertEqual(Token("+").is_add(), True)
        self.assertEqual(Token(">").is_branch_down(), True)
        self.assertEqual(Token("(").is_bracket_open(), True)
        self.assertEqual(Token(")").is_bracket_close(), True)
        self.assertEqual(Token("Test String").is_string(), True)

    def test_is_valid_closing_token(self):
        self.assertEqual(Token("+").is_valid_closing_token(), False)

        self.assertEqual(Token("Test").is_valid_closing_token(), True)
        self.assertEqual(Token(")").is_valid_closing_token(), True)

    def test_to_str(self):
        self.assertEqual(str(Token("Test")), "Test")
        self.assertEqual(str(Token("+")), "+")

    def test_equal_comparison(self):
        self.assertEqual(Token("+") == Token("+"), True)
        self.assertEqual(Token("+") == Token(">"), False)
        self.assertEqual(Token("+") == Token("++"), False)

        self.assertEqual(Token("Test") == Token("Test"), True)
        self.assertEqual(Token("Test") == Token("NoTest"), False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
