"""Test some jinja features"""

import unittest

import responses

from tests.helper import patch


class JinjaTest(unittest.TestCase):
    @responses.activate
    def test_include(self):
        self.assertEqual(
            patch("include/python-snippet.rst"),
            "def example():\n    print('Example')\n\n",
        )


if __name__ == "__main__":
    unittest.main()
