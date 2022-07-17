import importlib
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional, TypedDict

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pyproject_parser import PyProject


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


def read_cli_output(command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout + result.stderr


def read_func_output(function_spec: str) -> str:
    module, func_name = function_spec.rsplit(".", 1)
    func = getattr(importlib.import_module(module), func_name)
    return func()


template_functions = {"cli": read_cli_output, "func": read_func_output}


class Replacement:
    """A variable and its replacement text."""

    raw: str

    def __init__(self, raw: str):
        self.raw = raw.strip()

    def get(self) -> str:
        output: str
        if self.raw.startswith("cli:"):
            output = read_cli_output(self.raw[4:].strip())
        elif self.raw.startswith("func:"):
            output = read_func_output(self.raw[5:].strip())
        else:
            output = self.raw
        return str(output)


class FileConfig(TypedDict):
    src: str
    dest: str
    vars: Dict[str, str]
    parent: Path


class File:
    """A file to patch."""

    parent: Path
    src: str
    dest: str
    variables: Dict[str, str]

    def __init__(self, parent: Path, config: FileConfig):
        self.parent = parent
        self.src = config["src"]
        self.dest = config["dest"]
        self.variables = config["vars"]

    def patch(self):
        env = setup_template_env(self.parent)
        template = env.get_template(self.src)
        template.globals.update(template_functions)
        variables: Dict[str, str] = {}
        for k, v in self.variables.items():
            variables[k] = Replacement(v).get()
        rendered = template.render(**variables)
        dest = self.parent / self.dest
        dest.write_text(rendered)


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
