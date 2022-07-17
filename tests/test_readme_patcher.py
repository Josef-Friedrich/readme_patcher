import os
import tempfile
from typing import Optional
import unittest

from readme_patcher import patch_file, Variables


FILES_DIR = os.path.join(os.path.dirname(__file__), "files")


def create_tmp_file():
    return os.path.join(tempfile.mkdtemp(), os.path.basename("README.rst"))


def read_file_content(path: str):
    file = open(path, "r")
    return file.read()


def patch(src: str, variables: Optional[Variables] = None) -> str:
    tmp = create_tmp_file()
    patch_file(parent=FILES_DIR, src=src, dest=tmp, variables=variables)
    return read_file_content(tmp)


class ReadmePatcherTest(unittest.TestCase):
    def test_function_cli(self):
        self.assertEqual(patch("function_cli.rst"), "#output#")

    def test_filter_code(self):
        self.assertEqual(
            patch("filter_code.rst", {"output": "code"}),
            "#\n.. code-block:: \n\n    code\n\n#",
        )

    def test_filter_code_language(self):
        self.assertEqual(
            patch("filter_code_language.rst", {"output": "code"}),
            "#\n.. code-block:: python\n\n    code\n\n#",
        )
