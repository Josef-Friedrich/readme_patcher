import unittest


from readme_patcher.github import Github


class GithubTest(unittest.TestCase):
    github: Github = Github("https://github.com/Josef-Friedrich/readme_patcher/")

    def test_name(self):
        self.assertEqual(self.github.name, "readme_patcher")

    def test_full_name(self):
        self.assertEqual(self.github.full_name, "Josef-Friedrich/readme_patcher")

    def test_description(self):
        self.assertEqual(
            self.github.description,
            "Generate README files from templates. "
            "Allow input from functions calls and cli output.",
        )
