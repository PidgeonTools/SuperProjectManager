import os
from os import path as p


class Subfolders():
    def __init__(self, string):
        self.warnings = []
        self.recursion_level = 0

        self.string = string
        self.tokens = self.tokenize()
        self.tokens = self.stack_tokens()
        self.paths = self.compile_paths(self.tokens)
        self.display_paths = self.compile_display_paths(self.paths)

        if self.recursion_level != 0:
            self.warnings.append(
                "Unmatched Brackets detected! This might lead to unexpected behaviour when compiling paths!")

    # Tokenize a string with the syntax foo>>bar>>((spam>>eggs))++lorem++impsum
    # Possible Tokens: String token, branch down token >>, brackets (( and )), add token ++
    # Avoiding Regex. Instead, first envelope the tokens with the safe phrase ::safephrase.
    # This phrase won't occur in the string, so it can be safely used for splitting in the next step.
    # In the next step, the string is split up into all tokens by splitting up along ::safephrase
    # Finally, all empty strings are removed to avoid errors.
    def tokenize(self):
        self.string = self.string.replace(">>", "::safephrase>::safephrase")
        self.string = self.string.replace("++", "::safephrase+::safephrase")
        self.string = self.string.replace("((", "::safephrase(::safephrase")
        self.string = self.string.replace("))", "::safephrase)::safephrase")

        tokenized_string = self.string.split("::safephrase")
        tokenized_string = [el for el in tokenized_string if el != ""]

        return tokenized_string

    # Make sure subtrees opened and closed with brackets appear as single object.
    def stack_tokens(self):
        stacked_tokens = []
        while self.tokens:  # Using global self variable.
            token = self.tokens.pop(0)
            # Appends all elements from a subtree using recursion.
            if token == "(":
                self.recursion_level += 1
                stacked_tokens.append(self.stack_tokens())
            elif token == ")":  # Returns the current subtree as type list. This can be safely done, since it's working with recursion.
                self.recursion_level -= 1
                return stacked_tokens
            else:
                stacked_tokens.append(token)
        return stacked_tokens

    # Compile a list of stacked tokens into relative paths.
    def compile_paths(self, tokens):
        compiled_paths = []
        top_level_path = ""

        while tokens:
            token = tokens.pop(0)

            if type(token) == list:
                compiled_paths.extend(self.compile_paths(token))
            elif token == ">":
                try:
                    token = tokens.pop(0)
                except IndexError:
                    self.warnings.append(
                        "A string should end with a folder name, not with >> or ++!")
                    continue
                try:
                    top_level_path = compiled_paths[-1]
                except IndexError:
                    self.warnings.append(
                        "A >> can't be used until at least one Folder name is specified. This also applies for Brackets!")

                if type(token) == list:
                    for e in self.compile_paths(token):
                        compiled_paths.append(p.join(top_level_path, e))

                # In case of conflicting ++ and >> tokens, the >> token is preferred.
                elif token == "+":
                    self.warnings.append("A >> can't be followed by ++")
                    tokens.insert(0, "+")
                elif token == ">":
                    self.warnings.append("A >> can't be followed by >>")
                else:
                    compiled_paths.append(p.join(top_level_path, token))

            elif token == "+":
                try:
                    token = tokens.pop(0)
                except IndexError:
                    self.warnings.append(
                        "A string should end with a folder name, not with >> or ++!")
                    continue

                if type(token) == list:
                    for e in self.compile_paths(token):
                        compiled_paths.append(p.join(top_level_path, e))
                elif token == ">":
                    self.warnings.append("A ++ can't be followed by >>")
                    tokens.insert(0, ">")
                elif token == "+":
                    self.warnings.append("A ++ can't be followed by ++")
                else:
                    if top_level_path == "":
                        self.warnings.append(
                            "A ++ can't be used until at least one Folder name is specified and one >> is used. This also applies for Brackets!")
                    compiled_paths.append(p.join(top_level_path, token))
            else:
                compiled_paths.append(token)

        return compiled_paths

    def compile_display_paths(self, paths):
        display_paths = []

        for path in paths:
            display_path = path.replace("\\", ">>")
            display_path = display_path.replace("//", ">>")
            display_path = display_path.replace("/", ">>")

            display_paths.append(display_path)

        return display_paths
