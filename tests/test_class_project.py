"""Test some jinja features"""

import unittest

from .helper import project


class ClassProjectTest(unittest.TestCase):
    def test_property_py_project(self):

        rendered = project.patch()
        self.assertEqual(
            rendered[0],
            "README\n======\n\nhttps://github.com/Josef-Friedrich/readme_patcher\n",
        )
