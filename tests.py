# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from functions.json_functions import decode_json

from functions.path_generator import Subfolders


# -----------------------------------------------------------------------------
# Path Tests
# -----------------------------------------------------------------------------


def test_paths(test_cases=[]):
    path_tests = decode_json("test_cases.json")["path_tests"]

    if test_cases == []:
        test_cases = range(1, len(path_tests) + 1)

    for iteration, case in enumerate(path_tests):
        if iteration + 1 not in test_cases:
            continue
        expected = case["expected_result"]
        test_obj = Subfolders(case["case"])

        if test_obj.paths == expected["folders"]:
            print(
                f"Compiling Test {iteration + 1} passed: {test_obj.paths} is the expected result: {expected['folders']}\n")
        else:
            print(
                f"""#########################
Compiling Test {iteration + 1} failed: {test_obj.paths} is not the expected result: {expected['folders']}
#########################
""")

        if test_obj.warnings == expected["warnings"]:
            print(
                f"Warning Test {iteration + 1} passed: {test_obj.warnings} is the expected result: {expected['warnings']}\n\n\n")
        else:
            print(
                f"""#########################
Warning Test {iteration + 1} failed: {test_obj.warnings} is not the expected result: {expected['warnings']}
#########################


""")


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    test_paths([])
