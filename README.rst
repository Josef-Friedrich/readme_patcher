.. image:: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml
    :alt: Tests

readme_patcher
==============

Generate README files from templates. Allow input from functions calls and cli
output.

:: code-block:: shell

    cd your-project
    vim README_template.rst
    poetry add --group dev readme-patcher
    poetry shell
    readme-patcher # README.rst

Global objects
--------------

py_project
^^^^^^^^^^

.. code-block:: jinja

    {{ py_project.repository }}

github
^^^^^^

.. code-block:: jinja

    {{ github.name }}
    {{ github.full_name }}
    {{ github.description }}

Functions
---------

cli: Combined output (stdout and stderr) of command line interfaces (scripts / binaries)

.. code-block:: jinja

    {{ cli('awk --help') }}

func: return values of Python functions

.. code-block:: jinja

    {{ func('os.getcwd') }}

Filters
-------

code

.. code-block:: jinja

    {{ func('os.getcwd') | code }}

literal

.. code-block:: jinja

    {{ func('os.getcwd') | code }}

Configuration
-------------

.. code-block:: toml

    [[tool.readme_patcher.file]]
    src = "README_template.rst"
    dest = "README.rst"
    variables = { cwd = "func:os.getcwd", fortune = "cli:fortune --help" }
