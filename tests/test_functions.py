import os
import unittest

from .helper import patch, project, get_tmp_file_path


class FunctionsTest(unittest.TestCase):
    def test_cli(self):
        self.assertEqual(patch("functions/cli.rst"), "#output#\n")

    def test_func(self):
        self.assertEqual(patch("functions/func.rst"), "#{}#\n".format(os.getcwd()))

    def test_read(self):
        self.assertEqual(
            project.patch_file("read.rst", get_tmp_file_path()),
            "#\n:: \n\n    Example text\n\n#\n",
        )
