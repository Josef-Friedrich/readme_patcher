import os
import unittest


from tests.helper import get_tmp_file_path, patch, project, activate_requests_mock


class FunctionsTest(unittest.TestCase):
    @activate_requests_mock
    def test_cli(self):
        self.assertEqual(patch("functions/cli.rst"), "#output#\n")

    @activate_requests_mock
    def test_func(self):
        self.assertEqual(patch("functions/func.rst"), "#{}#\n".format(os.getcwd()))

    @activate_requests_mock
    def test_read(self):
        self.assertEqual(
            project.patch_file("read.rst", get_tmp_file_path()),
            "#\n:: \n\n    Example text\n\n#\n",
        )


if __name__ == "__main__":
    unittest.main()
