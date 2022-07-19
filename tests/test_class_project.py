"""Test some jinja features"""

from pathlib import Path
import unittest

from .helper import TEST_FILES_FOLDER
from readme_patcher import Project


class ClassProjectTest(unittest.TestCase):
    def test_property_py_project(self):
        project = Project(Path(TEST_FILES_FOLDER) / "project")
        rendered = project.patch()
        self.assertEqual(
            rendered[0],
            "README\n======\n\nhttps://github.com/Josef-Friedrich/readme_patcher\n",
        )
