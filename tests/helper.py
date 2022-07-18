import os
import tempfile
from typing import Optional

from readme_patcher import Project, Variables

FILES_DIR = os.path.join(os.path.dirname(__file__), "files")


def create_tmp_file():
    return os.path.join(tempfile.mkdtemp(), os.path.basename("README.rst"))


def read_file_content(path: str):
    file = open(path, "r")
    return file.read()


def patch(src: str, variables: Optional[Variables] = None) -> str:
    tmp = create_tmp_file()
    Project(FILES_DIR).patch_file(src=src, dest=tmp, variables=variables)
    return read_file_content(tmp)
