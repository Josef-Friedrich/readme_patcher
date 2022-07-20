import os
import unittest

from .helper import project, read_file_content, get_path


class BadgeTest(unittest.TestCase):
    def assert_patch_file(self, basename: str):
        rendered = project.patch_file(
            src="badge/{}_template.rst".format(basename),
            dest="badge/{}_tmp.rst".format(basename),
        )
        expected_rel_path = "project/badge/{}.rst".format(basename)
        expected = read_file_content(expected_rel_path)
        os.remove(get_path(expected_rel_path))
        self.assertEqual(rendered, expected)

    def test_pypi(self):
        self.assert_patch_file("pypi")

    def test_github_workflow(self):
        self.assert_patch_file("github_workflow")

    def test_readthedocs(self):
        self.assert_patch_file("readthedocs")
