import os
import subprocess
from typing import Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pyproject_parser import PyProject

env = Environment(loader=FileSystemLoader(os.getcwd()), autoescape=select_autoescape())




# def get_path(*path_segments: str) -> str:
#     return os.path.join(os.getcwd(), *path_segments)


# def read_file(path: str) -> str:
#     file = open(path, 'r')
#     content = file.read()
#     file.close()
#     return content

class FileToPatch:

    src: str
    dest: str
    variables: Dict[str, str]


def read_cli_output(command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


def patch():

    project =  PyProject().load('pyproject.toml')

    print(project.tool['readme_patcher'])
    # content = read_file('README_template.rst')
    template = env.get_template("README_template.rst")
    print(template.render(cli_output="lol"))
