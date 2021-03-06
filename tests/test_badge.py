import os
import unittest

from tests.helper import activate_requests_mock, get_path, project, read_file_content


class BadgeTest(unittest.TestCase):
    def assert_patch_file(self, basename: str):
        rendered = project.patch_file(
            src="badge/{}_template.rst".format(basename),
            dest="badge/{}_tmp.rst".format(basename),
        )
        expected = read_file_content("project/badge/{}.rst".format(basename))
        os.remove(get_path("project/badge/{}_tmp.rst".format(basename)))
        self.assertEqual(rendered, expected)

    @activate_requests_mock
    def test_pypi(self):
        self.assert_patch_file("pypi")

    @activate_requests_mock
    def test_github_workflow(self):
        self.assert_patch_file("github_workflow")

    @activate_requests_mock
    def test_readthedocs(self):
        self.assert_patch_file("readthedocs")


if __name__ == "__main__":
    unittest.main()
