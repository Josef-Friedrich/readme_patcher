import os
import unittest

import responses

from tests.helper import get_tmp_file_path, patch, project


class FunctionsTest(unittest.TestCase):
    @responses.activate
    def test_cli(self):
        self.assertEqual(patch("functions/cli.rst"), "#output#\n")

    @responses.activate
    def test_func(self):
        self.assertEqual(patch("functions/func.rst"), "#{}#\n".format(os.getcwd()))

    @responses.activate
    def test_read(self):
        self.assertEqual(
            project.patch_file("read.rst", get_tmp_file_path()),
            "#\n:: \n\n    Example text\n\n#\n",
        )


if __name__ == "__main__":
    unittest.main()
