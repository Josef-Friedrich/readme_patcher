import os
import subprocess


def get_path(*path_segments: str) -> str:
    return os.path.join(os.getcwd(), *path_segments)


def read_file(path: str) -> str:
    file = open(path, 'r')
    content = file.read()
    file.close()
    return content


def read_cli_output(command: str) -> str:
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout


def patch():
    print('patch')
