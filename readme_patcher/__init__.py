import os
from pathlib import Path
from typing import Dict, Optional, TypedDict

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pyproject_parser import PyProject

from . import functions, filters


def setup_template_env(pwd: os.PathLike[str]) -> Environment:
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
    parent: Path


Variables = Dict[str, str]


class File:
    """A file to patch."""

    parent: Path
    src: str
    dest: str
    variables: Optional[Variables] = None

    def __init__(
        self,
        parent: Path,
        src: Optional[str] = None,
        dest: Optional[str] = None,
        variables: Optional[Variables] = None,
        config: Optional[FileConfig] = None,
    ):
        self.parent = parent
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
        env = setup_template_env(self.parent)
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
        dest = self.parent / self.dest
        dest.write_text(rendered)
        return rendered


def patch_file(
    parent: str, src: str, dest: str, variables: Optional[Variables] = None
) -> str:
    return File(parent=Path(parent), src=src, dest=dest, variables=variables).patch()


def patch():
    pyproject_toml = search_for_pyproject_toml()

    if not pyproject_toml:
        raise Exception("No pyproject.toml file found.")

    project = PyProject().load(pyproject_toml)

    if not project.tool["readme_patcher"]:
        raise Exception("No tools.readme_patcher section")

    config = project.tool["readme_patcher"]

    for file_config in config["file"]:
        file = File(pyproject_toml.parent, file_config)
        file.patch()
