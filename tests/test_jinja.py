"""Test some jinja features"""

import unittest


from tests.helper import patch, activate_requests_mock


class JinjaTest(unittest.TestCase):
    @activate_requests_mock
    def test_include(self):
        self.assertEqual(
            patch("include/python-snippet.rst"),
            "def example():\n    print(\"Example\")\n\n",
        )


if __name__ == "__main__":
    unittest.main()
