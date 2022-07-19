.. image:: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml
    :alt: Tests

readme_patcher
==============

{{ github.description | wordwrap }}

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
{% raw %}
    {{ py_project.repository }}
{% endraw %}

github
^^^^^^

.. code-block:: jinja
{% raw %}
    {{ github.name }}
    {{ github.full_name }}
    {{ github.description }}
{% endraw %}

Functions
---------

cli: Combined output (stdout and stderr) of command line interfaces (scripts / binaries)

.. code-block:: jinja
{% raw %}
    {{ cli('awk --help') }}
{% endraw %}

func: return values of Python functions

.. code-block:: jinja
{% raw %}
    {{ func('os.getcwd') }}
{% endraw %}

Filters
-------

code

.. code-block:: jinja
{% raw %}
    {{ func('os.getcwd') | code }}
{% endraw %}

literal

.. code-block:: jinja
{% raw %}
    {{ func('os.getcwd') | code }}
{% endraw %}

Configuration
-------------

.. code-block:: toml

    [[tool.readme_patcher.file]]
    src = "README_template.rst"
    dest = "README.rst"
    variables = { cwd = "func:os.getcwd", fortune = "cli:fortune --help" }
