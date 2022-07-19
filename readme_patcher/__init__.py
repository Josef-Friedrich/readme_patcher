from __future__ import annotations

import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, TypedDict

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pyproject_parser import PyProject

from . import filters, functions
from .github import Github


def setup_template_env(search_path: "os.PathLike[str]") -> Environment:
    """
    Setup the search paths for the template engine Jinja2. ``os.path.sep`` is
    required to be able to include absolute paths, quotes around
    ``os.PathLike[str]`` to get py38 compatibility."""
    return Environment(
        loader=FileSystemLoader([search_path, os.path.sep]),
        autoescape=select_autoescape(),
        keep_trailing_newline=True,
    )


def search_for_pyproject_toml() -> Optional[Path]:
    """
    https://stackoverflow.com/a/68994012
    """
    directory = Path.cwd()
    # /
    root = Path(directory.root)
    while directory != root:
        attempt = directory / "pyproject.toml"
        if attempt.exists():
            return attempt
        directory = directory.parent
    return None


class Replacement:
    """A variable and its replacement text."""

    raw: str

    def __init__(self, raw: str):
        self.raw = raw.strip()

    def get(self) -> str:
        output: str
        if self.raw.startswith("cli:"):
            output = functions.read_cli_output(self.raw[4:].strip())
        elif self.raw.startswith("func:"):
            output = functions.read_func_output(self.raw[5:].strip())
        else:
            output = self.raw
        return str(output)


class FileConfig(TypedDict):
    src: str
    dest: str
    variables: Dict[str, str]


Variables = Dict[str, str]


class File:
    """A file to patch."""

    project: Project
    src: str
    dest: str
    variables: Optional[Variables] = None

    def __init__(
        self,
        project: Project,
        src: Optional[str] = None,
        dest: Optional[str] = None,
        variables: Optional[Variables] = None,
        config: Optional[FileConfig] = None,
    ):
        self.project = project
        if config:
            self.src = config["src"]
            self.dest = config["dest"]
            self.variables = config["variables"]
        if src:
            self.src = src
        if dest:
            self.dest = dest
        if variables:
            self.variables = variables

    def _setup_template(self) -> Template:
        env = setup_template_env(self.project.base_dir)
        env.filters.update(filters.collection)  # type: ignore
        template = env.get_template(self.src)
        template.globals.update(functions.collection)
        if self.project.py_project:
            template.globals.update(py_project=self.project.py_project)
            if self.project.py_project.repository:
                try:
                    github = Github(self.project.py_project.repository)
                    template.globals.update(github=github)
                except Exception:
                    pass
        return template

    def patch(self) -> str:
        template = self._setup_template()
        variables: Dict[str, str] = {}
        if self.variables:
            for k, v in self.variables.items():
                variables[k] = Replacement(v).get()
        rendered = template.render(**variables)
        # Remove multiple newlines
        rendered = re.sub(r"\n\s*\n", "\n\n", rendered)
        dest = self.project.base_dir / self.dest
        dest.write_text(rendered)
        return rendered


class SimplePyProject:

    py_project: PyProject

    """Contain the attributes of a pyproject.toml file that interest us"""

    def __init__(self, py_project: PyProject):
        self.py_project = py_project

    @property
    def repository(self) -> str | None:
        if self.py_project.tool and self.py_project.tool["poetry"]["repository"]:
            return self.py_project.tool["poetry"]["repository"]


class Project:
    """A project corresponds to a code repository. In its root there is a
    README file."""

    base_dir: Path

    def __init__(self, base_dir: str | Path):
        if isinstance(base_dir, str):
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = base_dir

    @property
    def _py_project(self) -> PyProject | None:
        """"""
        path = self.base_dir / "pyproject.toml"
        if path.exists():
            return PyProject().load(path)  # type: ignore

    @property
    def py_project(self) -> SimplePyProject | None:
        py_project = self._py_project
        if py_project:
            return SimplePyProject(py_project)

    @property
    def py_project_config(self) -> Dict[str, Any] | None:
        if self._py_project and "readme_patcher" in self._py_project.tool:
            return self._py_project.tool["readme_patcher"]

    def patch_file(
        self, src: str, dest: str, variables: Optional[Variables] = None
    ) -> str:
        return File(project=self, src=src, dest=dest, variables=variables).patch()

    def _patch_files_specified_in_toml(self, config: Dict[str, Any]) -> List[str]:
        rendered: List[str] = []
        for file_config in config["file"]:
            file = File(project=self, config=file_config)
            rendered.append(file.patch())
        return rendered

    def _patch_default(self) -> str:
        return File(project=self, src="README_template.rst", dest="README.rst").patch()

    def patch(self) -> List[str]:
        config = self.py_project_config
        if config:
            return self._patch_files_specified_in_toml(config)
        else:
            return [self._patch_default()]


def main():
    pyproject_toml = search_for_pyproject_toml()
    base_dir: str | Path
    if pyproject_toml:
        base_dir = pyproject_toml.parent
    else:
        base_dir = os.getcwd()

    print("Found project in {}".format(base_dir))

    Project(base_dir).patch()
