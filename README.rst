.. image:: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/readme_patcher/actions/workflows/tests.yml
    :alt: Tests

readme_patcher
==============

Generate README files from templates. Allow input from functions calls and cli output.

.. code-block:: jinja

    {{ cli('awk --help') | code }}
