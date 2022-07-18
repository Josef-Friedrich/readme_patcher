"""Custom jinja filters

https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters
"""

from jinja2.filters import do_indent


def _indent_block(content: str) -> str:
    return "\n\n" + do_indent(content.strip(), width=4, first=True) + "\n\n"


def wrap_in_code_block(content: str, language: str = "") -> str:
    """https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-code-block

    https://pygments.org/docs/lexers/
    """
    return "\n.. code-block:: " + language + _indent_block(content)


def wrap_in_literal_block(content: str) -> str:
    """
    https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#literal-blocks
    """
    return "\n:: " + _indent_block(content)


collection = {"code": wrap_in_code_block, "literal": wrap_in_literal_block}
