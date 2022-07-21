"""Test some jinja features"""

import unittest

import responses

from tests.helper import project


class ClassProjectTest(unittest.TestCase):
    @responses.activate
    def test_property_py_project(self):
        rendered = project.patch()
        self.assertEqual(
            rendered[0],
            "README\n======\n\nhttps://github.com/Josef-Friedrich/readme_patcher\n",
        )


if __name__ == "__main__":
    unittest.main()
