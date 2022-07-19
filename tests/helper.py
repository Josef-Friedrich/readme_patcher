import os
from pathlib import Path
import tempfile
from typing import Optional

from readme_patcher import Project, Variables

TEST_FILES_FOLDER = os.path.join(os.path.dirname(__file__), "files")


def create_tmp_file():
    return os.path.join(tempfile.mkdtemp(), os.path.basename("README.rst"))


def read_file_content(path: str):
    file = open(path, "r")
    return file.read()


def patch(src: str, variables: Optional[Variables] = None) -> str:
    tmp = create_tmp_file()
    Project(TEST_FILES_FOLDER).patch_file(src=src, dest=tmp, variables=variables)
    return read_file_content(tmp)


def get_project() -> Project:
    return Project(Path(TEST_FILES_FOLDER) / "project")
