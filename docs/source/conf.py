# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# mypy: disable-error-code="var-annotated"

# Portions from:
# https://github.com/mahmoud/boltons/blob/master/docs/conf.py
# https://github.com/melissawm/minimalsphinx/blob/main/docs/conf.py

import sys

from path import Path

CUR_DIR = Path(__file__).absolute().parent  # file parent is directory
PROJECT_PATH = CUR_DIR.parent.absolute()
EXTRA_PYTHON_PATH = PROJECT_PATH / "src"
sys.path.insert(0, EXTRA_PYTHON_PATH)

import git_objview  # noqa: E402

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "git-objview"
copyright = "2025, Jevin Sweval"
author = "Jevin Sweval"
release = git_objview.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    # "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_immaterial",
    # "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "sphinx_rtd_theme"
html_theme = "sphinx_immaterial"

if html_theme == "sphinx_immaterial":
    html_theme_options = {
        "features": ["toc.follow"],
    }

html_static_path = ["_static"]

intersphinx_mapping = {
    "c.pygit2": ("https://www.pygit2.org", None),
}
