import typing

if typing.TYPE_CHECKING:
    from . import Project


class Badge:

    project: 'Project'

    def __init__(self, project: 'Project'):
        self.project = project

    def github_workflow(self, workflow: str = "tests"):
        github = self.project.github
        if not github:
            raise Exception("No github repo found")
        url = "https://github.com/{}/actions/workflows/{}.yml".format(
            github.full_name, workflow
        )

        return (
            ".. image:: {}/badge.svg\n".format(url)
            + "    :target: {}\n".format(url)
            + "    :alt: Tests"
        )
