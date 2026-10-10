"""Sphinx configuration for the sphinx-jsonschema demo project.

Deliberately minimal: default theme, no jsonschema_options, so that every
visible difference comes from the directive options used in index.rst.
"""

project = 'sphinx-jsonschema demo'
author = 'sphinx-jsonschema contributors'
copyright = '2017-2026, sphinx-jsonschema contributors'

extensions = ['sphinx-jsonschema']

master_doc = 'index'
exclude_patterns = ['_build', 'README.md']

# The default table style includes 'colorrows', which aborts with "TeX capacity
# exceeded" on every table with Sphinx 9.1 and TeX Live 2026 (independent of this plugin).
latex_table_style = ['booktabs']
latex_elements = { 
    "papersize": "a4paper",
    "extraclassoptions": "oneside,openany",
    'fncychap': ""
}
latex_documents = [
    (master_doc, 'sphinx-jsonschema-demo.tex', 'sphinx-jsonschema demo', author, 'manual'),
]
