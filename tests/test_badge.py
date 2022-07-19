import unittest

from .helper import get_project


class BadgeTest(unittest.TestCase):
    def test_pypi(self):
        project = get_project()
        rendered = project.patch_file(
            src="badge/pypi_template.rst", dest="badge/pypi.rst"
        )
        self.assertEqual(
            rendered,
            """#.. image:: http://img.shields.io/pypi/v/readme-patcher.svg
    :target: https://pypi.org/project/readme-patcher
    :alt: This package on the Python Package Index
#
""",
        )

    def test_github_workflow(self):
        project = get_project()
        rendered = project.patch_file(
            src="badge/github_workflow_template.rst", dest="badge/github_workflow.rst"
        )
        self.assertEqual(
            rendered,
            """#.. image:: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/test.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/test.yml
    :alt: Tests
#
""",
        )
