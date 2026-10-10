# Demo document

A small Sphinx project that demonstrates the `jsonschema` directive. 
It exists to check features and their visual result by eye; it is not part of the published documentation.

Build it with tox (none of these environments is part of the default `envlist`):

| Command | Result |
|---|---|
| `tox -e demo-html` | `demo/_build/html/index.html` |
| `tox -e demo-latex` | LaTeX sources in `demo/_build/latex` |
| `tox -e demo-pdf` | HTML plus `demo/_build/latex/sphinx-jsonschema-demo.pdf` (needs `latexmk`) |

Pass extra Sphinx arguments after `--`, for example `tox -e demo-html -- -W` to turn warnings into errors.

## Layout

- `index.rst` - the demo document: (1) minimal example, (2) configuration variations, (3) schema elements.
- `schemas/` - every schema as a separate file, included by file name. Never inline.
- `conf.py` - minimal configuration, default theme, no global `jsonschema_options`.

To add a feature, put a schema into `schemas/` and add a section with a short introduction to `index.rst`. 
