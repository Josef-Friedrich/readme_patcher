import unittest

from readme_patcher.github import GithubRepository, request_github_api
from tests.helper import activate_requests_mock, project


class GithubTest(unittest.TestCase):
    github: GithubRepository = request_github_api(
        "https://github.com/Josef-Friedrich/readme_patcher/"
    )

    @activate_requests_mock
    def test_name(self):
        self.assertEqual(self.github["name"], "readme_patcher")

    @activate_requests_mock
    def test_full_name(self):
        self.assertEqual(self.github["full_name"], "Josef-Friedrich/readme_patcher")

    @activate_requests_mock
    def test_description(self):
        self.assertEqual(
            self.github["description"],
            "Generate README files from templates. "
            "Allow input from functions calls and cli output.",
        )

    @activate_requests_mock
    def test_integration(self):
        self.assertEqual(
            project.patch_file(
                src="objects/github/owner/login_template.rst",
                dest="objects/github/owner/login.rst",
            ),
            "#Josef-Friedrich#\n",
        )
