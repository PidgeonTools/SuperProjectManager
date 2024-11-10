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


from os import path as p

import sys
sys.path.append(p.dirname(p.dirname(__file__)))

if True:
    from objects.token import Token


def test_token_type():
    assert Token("+").is_add()
    assert Token(">").is_branch_down()
    assert Token("(").is_bracket_open()
    assert Token(")").is_bracket_close()
    assert Token("Test String").is_string()

    assert not Token("String").is_add()
    assert not Token("String").is_branch_down()
    assert not Token("String").is_bracket_open()
    assert not Token("String").is_bracket_close()
    assert not Token(">").is_string()


def test_is_valid_closing_token():
    assert not Token("+").is_valid_closing_token()
    assert not Token(">").is_valid_closing_token()
    assert not Token("(").is_valid_closing_token()

    assert Token("Test").is_valid_closing_token()
    assert Token(")").is_valid_closing_token()


def test_to_str():
    assert str(Token("Test")) == "Test"
    assert str(Token("+")) == "+"


def test_equal_comparison():
    assert Token("+") == Token("+")
    assert not Token("+") == Token(">")
    assert not Token("+") == Token("++")

    assert Token("Test") == Token("Test")
    assert not Token("Test") == Token("NoTest")
