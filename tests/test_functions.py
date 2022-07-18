import os
import unittest

from .helper import patch


class FunctionsTest(unittest.TestCase):
    def test_cli(self):
        self.assertEqual(patch("functions/cli.rst"), "#output#")

    def test_func(self):
        self.assertEqual(patch("functions/func.rst"), "#{}#".format(os.getcwd()))

    def test_include(self):
        self.assertEqual(
            patch("include/python-snippet.rst"), "def example():\n    print('Example')"
        )
