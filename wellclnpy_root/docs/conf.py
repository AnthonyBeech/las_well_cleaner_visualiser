# Configuration file for the Sphinx documentation builder.
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
project = 'wellclnpy'
copyright = '2023, Anthony Beech'
author = 'Anthony Beech'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
