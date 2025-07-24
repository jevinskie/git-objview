# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Portions from: https://github.com/mahmoud/boltons/blob/master/docs/conf.py

import sys

from path import Path

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
CUR_PATH = Path(__file__).absolute().parent  # file parent is directory
PROJECT_PATH = CUR_PATH.parent.absolute()
EXTRA_PYTHON_PATH = PROJECT_PATH / "src"
PACKAGE_PATH = EXTRA_PYTHON_PATH / "git_objview"
sys.path.insert(0, EXTRA_PYTHON_PATH)
# sys.path.insert(0, PACKAGE_PATH)

print(f"CUR_PATH: {CUR_PATH} PROJ: {PROJECT_PATH} EXTRA: {EXTRA_PYTHON_PATH} PKG: {PACKAGE_PATH}")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "git-objview"
copyright = "2025, Jevin Sweval"
author = "Jevin Sweval"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

autosummary_generate = True

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

import git_objview  # noqa: E402

release = git_objview.__version__
