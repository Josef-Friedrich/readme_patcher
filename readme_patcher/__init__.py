from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional, TypedDict

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pyproject_parser import PyProject

from . import filters, functions


def setup_template_env(pwd: "os.PathLike[str]") -> Environment:
    """Quotes around os.PathLike[str] to get py38 compatibility."""
    return Environment(loader=FileSystemLoader(pwd), autoescape=select_autoescape())


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

    base_dir: Path
    src: str
    dest: str
    variables: Optional[Variables] = None

    def __init__(
        self,
        base_dir: Path,
        src: Optional[str] = None,
        dest: Optional[str] = None,
        variables: Optional[Variables] = None,
        config: Optional[FileConfig] = None,
    ):
        self.base_dir = base_dir
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
        env = setup_template_env(self.base_dir)
        env.filters.update(filters.collection)
        template = env.get_template(self.src)
        template.globals.update(functions.collection)
        return template

    def patch(self) -> str:
        template = self._setup_template()

        variables: Dict[str, str] = {}
        if self.variables:
            for k, v in self.variables.items():
                variables[k] = Replacement(v).get()
        rendered = template.render(**variables)
        dest = self.base_dir / self.dest
        dest.write_text(rendered)
        return rendered


class Project:
    base_dir: Path

    def __init__(self, base_dir: str | Path):
        if isinstance(base_dir, str):
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = base_dir

    @property
    def pyproject_toml(self) -> Path:
        return self.base_dir / "pyproject.toml"

    @property
    def has_pyproject_toml(self) -> bool:
        return self.pyproject_toml.exists()

    def patch_file(
        self, src: str, dest: str, variables: Optional[Variables] = None
    ) -> str:
        return File(
            base_dir=self.base_dir, src=src, dest=dest, variables=variables
        ).patch()

    def _patch_files_specified_in_toml(self, project: PyProject) -> None:
        if not project.tool["readme_patcher"]:
            raise Exception("No tools.readme_patcher section")
        config = project.tool["readme_patcher"]

        for file_config in config["file"]:
            file = File(self.base_dir, file_config)
            file.patch()

    def _patch_default(self):
        File(
            base_dir=self.base_dir, src="README_template.rst", dest="README.rst"
        ).patch()

    def patch(self):
        if self.has_pyproject_toml:
            project = PyProject().load(self.pyproject_toml)
            self._patch_files_specified_in_toml(project)
        else:
            self._patch_default()


def main():
    pyproject_toml = search_for_pyproject_toml()
    base_dir: str | Path
    if pyproject_toml:
        base_dir = pyproject_toml
    else:
        base_dir = os.getcwd()

    print(base_dir)

    Project(base_dir).patch()
