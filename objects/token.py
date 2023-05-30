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

class Token():
    def __init__(self, value: str) -> None:
        self.value = value
        self.type = "STRING"

        if value == ">":
            self.type = "BRANCH_DOWN"

        if value == "(":
            self.type = "BRACKET_OPEN"

        if value == ")":
            self.type = "BRACKET_CLOSE"

        if value == "+":
            self.type = "ADD"

    def __str__(self) -> str:
        return self.value

    def __eq__(self, __value: 'Token') -> bool:
        return self.value == __value.value

    def is_string(self) -> bool:
        return self.type == "STRING"

    def is_branch_down(self) -> bool:
        return self.type == "BRANCH_DOWN"

    def is_bracket_open(self) -> bool:
        return self.type == "BRACKET_OPEN"

    def is_bracket_close(self) -> bool:
        return self.type == "BRACKET_CLOSE"

    def is_add(self) -> bool:
        return self.type == "ADD"

    def is_valid_closing_token(self) -> bool:
        return self.type in ["STRING", "BRACKET_CLOSE"]
