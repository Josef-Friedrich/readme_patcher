import typing
from typing import Optional

if typing.TYPE_CHECKING:
    from . import Project


class Badge:

    project: "Project"

    def __init__(self, project: "Project"):
        self.project = project

    def _linked_image(self, image: str, link: str, alt: Optional[str] = None):
        markup = ".. image:: {}\n".format(image) + "    :target: {}\n".format(link)
        if alt:
            markup += "    :alt: {}\n".format(alt)
        return markup

    def pypi(self):
        py_project = self.project.py_project
        if not py_project:
            raise Exception("No pyproject.toml")
        return self._linked_image(
            "http://img.shields.io/pypi/v/{}.svg".format(py_project.name_normalized),
            "https://pypi.org/project/{}".format(py_project.name_normalized),
            "This package on the Python Package Index",
        )

    def github_workflow(self, workflow: str = "tests", alt: Optional[str] = None):
        github = self.project.github
        if not github:
            raise Exception("No github repo found")
        url = "https://github.com/{}/actions/workflows/{}.yml".format(
            github.full_name, workflow
        )
        return self._linked_image(url + "/badge.svg", url, alt)
