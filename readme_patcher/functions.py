"""https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters"""


import importlib
import subprocess


def read_cli_output(command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = result.stdout + result.stderr
    return output.strip()


def read_func_output(function_spec: str) -> str:
    module, func_name = function_spec.rsplit(".", 1)
    func = getattr(importlib.import_module(module), func_name)
    return func()


collection = {"cli": read_cli_output, "func": read_func_output}
