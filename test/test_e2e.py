import unittest
import tempfile
from pathlib import Path
import nbformat
import sys
from io import StringIO
from unittest.mock import patch

from content_test_enforcer import cli_entry_point

example_notebooks = {
    "good": "test/example-notebooks/pass.ipynb",
    "bad": "test/example-notebooks/fail.ipynb",
}


class TestCLI(unittest.TestCase):
    @patch("sys.stdout", StringIO())
    @patch("sys.argv", ["content-test-enforcer", example_notebooks["bad"]])
    def test_fail_scenario(self):
        with self.assertRaises(SystemExit) as context:
            cli_entry_point()
        self.assertEqual(context.exception.code, 1)

    @patch("sys.stdout", StringIO())
    @patch("sys.argv", ["content-test-enforcer", example_notebooks["good"]])
    def test_pass_scenario(self):
        with self.assertRaises(SystemExit) as context:
            cli_entry_point()
        self.assertEqual(context.exception.code, 0)


if __name__ == "__main__":
    unittest.main(buffer=True)
