#!/usr/bin/env python3

""" This module will run the test suite of the selected game."""

import difflib
import subprocess
import pathlib
import sys
import re


class SolutionNotFoundError(Exception):
    """Missing solution.py file."""


class MissingTestOutputError(Exception):
    """Raised when a missing test output is detected."""

    def __init__(self, test_input, test_output):
        super().__init__()
        self.test_input = test_input
        self.test_output = test_output

    def __str__(self):
        return (
            f"Cannot find the test output '{self.test_output}' "
            "associated to the test input '{self.test_input}'"
        )


class NotExpectedOutputError(Exception):
    """Raised when the solution.py does not output what is expected."""

    def __init__(self, diffs):
        super().__init__()
        self.diffs = diffs

    def __str__(self):
        return "Diff between your output and the expected output:\n" + "\n".join(
            self.diffs
        )


def run(game_dir):
    """Run all the tests contained in a game."""

    solution = game_dir / "solution.py"
    if not solution.exists():
        raise SolutionNotFoundError()
    test_suite = {}
    for input_test in game_dir.glob("input_*.txt"):
        output_test_filename = input_test.name.replace("input_", "output_")
        output_test = game_dir / output_test_filename
        if not output_test.exists():
            raise MissingTestOutputError(input_test, output_test)
        test_suite[input_test] = output_test
    for input_test, output_test in test_suite.items():
        print(f"Running '{input_test}': ", end="")
        output = None
        expected_output = None
        with input_test.open(encoding="utf-8") as input_file:
            completed = subprocess.run(
                ["python3", solution.absolute()],
                capture_output=True,
                stdin=input_file,
                check=True,
            )
            output = completed.stdout.decode("utf-8").splitlines()

        with output_test.open(encoding="utf-8") as output_file:
            expected_output = [s.strip() for s in output_file.readlines()]

        diff = difflib.Differ()
        diffs = list(diff.compare(output, expected_output))
        if len(diffs) != len(expected_output):
            print("FAIL")
            raise NotExpectedOutputError(diffs)
        print("OK")


def main():
    """Entrypoint."""

    if len(sys.argv) != 2:
        print("Missing the game to start")
        sys.exit(1)
    game_to_run = sys.argv[1]
    if re.match(r"^[0-9]{4}", game_to_run) is None:
        print(f"Game [{game_to_run}] should be 4-digits string")
        sys.exit(1)

    root_path = pathlib.Path(".")
    selected_game_dir = None
    for game_dir in root_path.iterdir():
        if game_dir.name.startswith(game_to_run):
            selected_game_dir = game_dir
            break
    if selected_game_dir is None:
        print(f"Game [{game_to_run}] cannot be found")
        sys.exit(1)

    try:
        run(selected_game_dir)
    except Exception as err:
        print(f"Your solution does not work. Error: {err}")
        sys.exit(1)
    else:
        print("Bravo")


if __name__ == "__main__":
    main()
