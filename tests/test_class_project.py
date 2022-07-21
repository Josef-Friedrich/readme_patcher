"""Test some jinja features"""

import unittest


from tests.helper import project, activate_requests_mock


class ClassProjectTest(unittest.TestCase):
    @activate_requests_mock
    def test_property_py_project(self):
        rendered = project.patch()
        self.assertEqual(
            rendered[0],
            "README\n======\n\nhttps://github.com/Josef-Friedrich/readme_patcher\n",
        )


if __name__ == "__main__":
    unittest.main()
