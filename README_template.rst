{{ badge.pypi }}

{{ badge.github_workflow() }}

readme_patcher
==============

{{ github.description | wordwrap }}

.. code-block:: shell

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


badge
^^^^^

.. code-block:: jinja
{% raw %}
    {{ badge.pypi }}
    {{ badge.github_workflow('tests' 'Tests') }}
    {{ badge.readthedocs }}
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

read: read text files

.. code-block:: jinja
{% raw %}
    {{ read('code/example.py') | code('python') }}
{% endraw %}

Filters
-------

code

.. code-block:: jinja
{% raw %}
    {{ 'print("example")' | code('python') }}
{% endraw %}

::

    .. code-block:: python

        print("example")

literal

.. code-block:: jinja
{% raw %}
    {{ func('os.getcwd') | literal }}
{% endraw %}

::

    ::

        /home/repos/project

Configuration
-------------

.. code-block:: toml

    [[tool.readme_patcher.file]]
    src = "README_template.rst"
    dest = "README.rst"
    variables = { cwd = "func:os.getcwd", fortune = "cli:fortune --help" }
