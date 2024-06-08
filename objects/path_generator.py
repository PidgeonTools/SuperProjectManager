import os
from os import path as p

import typing

from .. import (
    __package__
)


try:
    from .token import Token
    from ..addon_types import AddonPreferences
    from bpy.types import (
        Context
    )
except:
    import sys
    sys.path.append(p.dirname(p.dirname(__file__)))
    from objects.token import Token


class Subfolders():
    def __init__(self, string: str, prefix: str = ""):
        self.prefix = prefix
        self.tree = {}
        self.warnings = []

        self._return_from_close_bracket = False

        self.tokens = self.tokenize(string)
        if len(self.tokens) == 0:
            return

        self.tree = self.parse_tree()

    def __str__(self) -> str:
        """Return a string representation of the folder tree."""
        return "/\n" + self.__to_string(self.tree)

    def __to_string(self, subtree: dict = None, row_prefix: str = "") -> str:
        """Recursive helper function for __str__()."""

        # Unicode characters for the tree represantation.
        UNICODE_RIGHT = "\u2514"
        UNICODE_VERTICAL_RIGHT = "\u251C"
        UNICODE_VERTICAL = "\u2502"

        return_string = ""

        folders = subtree.keys()

        for i, folder in enumerate(folders):
            unicode_prefix = UNICODE_VERTICAL_RIGHT + " "
            row_prefix_addition = UNICODE_VERTICAL + " "

            if i == len(folders) - 1:
                unicode_prefix = UNICODE_RIGHT + " "
                row_prefix_addition = "  "

            return_string += row_prefix + unicode_prefix + self.prefix + folder + "\n"

            return_string += self.__to_string(subtree.get(folder,
                                                          {}), row_prefix + row_prefix_addition)

        return return_string

    def tokenize(self, string: str):
        """Tokenize a string with the syntax foo>>bar>>((spam>>eggs))++lorem++impsum
        Possible Tokens: String token, branch down token >>, brackets (( and )), add token ++
        Avoiding Regex. Instead, first envelope the tokens with the safe phrase ::safephrase.
        This phrase won't occur in the string, so it can be safely used for splitting in the next step.
        In the next step, the string is split up into all tokens by splitting up along ::safephrase
        Finally, all empty strings are removed to avoid errors."""

        string = string.replace(">>", "::safephrase>::safephrase")
        string = string.replace("++", "::safephrase+::safephrase")
        string = string.replace("((", "::safephrase(::safephrase")
        string = string.replace("))", "::safephrase)::safephrase")

        tokenized_string = string.split("::safephrase")
        if tokenized_string.count("(") != tokenized_string.count(")"):
            self.warnings.append(
                "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!")

        tokens = [Token(el) for el in tokenized_string if el != ""]

        return tokens

    def parse_tree(self):
        """Parse tokens as tree of paths."""
        tree: dict = {}
        active_folder = ""

        if not self.tokens[-1].is_valid_closing_token():
            last_token = str(self.tokens.pop()) * 2
            self.warnings.append(
                f"A folder path should not end with '{last_token}'!")

        while self.tokens:
            if self._return_from_close_bracket:
                return tree

            token = self.tokens.pop(0)

            if token.is_string():
                tree[str(token)] = {}
                active_folder = str(token)
                continue

            if token.is_branch_down():
                if active_folder == "":
                    self.warnings.append(
                        "A '>>' can't be used until at least one Folder name is specified! This rule also applies for subfolders.")
                    continue

                tree[active_folder] = self.parse_tree()
                continue

            if token.is_bracket_open():
                tree.update(self.parse_tree())

                self._return_from_close_bracket = False
                continue

            if token.is_bracket_close():
                self._return_from_close_bracket = True
                return tree

        return tree

    def compile_paths(self, subpath: str = "", subtree: dict = None,) -> typing.List[str]:
        """Compile the Tree into a list of relative paths."""
        paths = []

        if subtree is None:
            subtree = self.tree

        for folder in subtree.keys():
            path = p.join(subpath, self.prefix + folder)
            paths.append(path)

            paths.extend(self.compile_paths(path, subtree.get(folder, {})))

        return paths

    def build_folders(self, project_dir: str) -> None:
        """Create the folders on the system."""
        for path in self.compile_paths(project_dir):

            if not p.isdir(path):
                os.makedirs(path)


def subfolder_enum(self, context: 'Context'):
    prefs: 'AddonPreferences' = context.preferences.addons[__package__].preferences

    tooltip = "Select Folder as target folder for your Blender File. \
Uses Folders from Automatic Setup."
    items = [(" ", "Root", tooltip)]

    folders = self.automatic_folders
    if context.scene.project_setup == "Custom_Setup":
        folders = self.custom_folders

    prefix = ""
    if prefs.prefix_with_project_name:
        prefix = context.scene.project_name + "_"

    try:
        for folder in folders:
            for subfolder in Subfolders(folder.folder_name, prefix).compile_paths():
                # subfolder = subfolder.replace(
                #     "/", ">>").replace("//", ">>").replace("\\", ">>")
                items.append(
                    (subfolder, subfolder.replace(prefix, ""), tooltip))
    except Exception as e:
        print("Exception in function subfolder_enum")
        print(e)

    return items
