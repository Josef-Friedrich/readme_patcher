import unittest


from tests.helper import patch, activate_requests_mock


class FiltersTest(unittest.TestCase):
    @activate_requests_mock
    def test_filter_code(self):
        self.assertEqual(
            patch("filters/code/without-language.rst", {"output": "code"}),
            "#\n.. code-block:: \n\n    code\n\n#\n",
        )

    @activate_requests_mock
    def test_filter_code_language(self):
        self.assertEqual(
            patch("filters/code/with-language.rst", {"output": "code"}),
            "#\n.. code-block:: python\n\n    code\n\n#\n",
        )

    @activate_requests_mock
    def test_literal(self):
        self.assertEqual(
            patch("filters/literal.rst", {"output": "code"}),
            "#\n:: \n\n    code\n\n#\n",
        )

    @activate_requests_mock
    def test_heading(self):
        self.assertEqual(
            patch("filters/heading.rst"),
            "#\nheading\n=======\n#\n",
        )


if __name__ == "__main__":
    unittest.main()
