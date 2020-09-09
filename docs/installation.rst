
Installation
============

Obtain sphinx-jsonschema by installing it with pip:

.. code-block:: bash

    sudo pip install sphinx-jsonschema

Then add it to your project by editing the ``conf.py`` file and
append 'sphinx-jsonschema' to the ``extensions`` array.

.. code-block:: python

    extensions = [
        'sphinx.ext.autodoc',
        'sphinx-jsonschema'
    ]

Source code
-----------

The source code for this extension can be found on `GitHub <https://github.com/lnoor/sphinx-jsonschema>`_.

Docker image
------------

A Docker image containing Sphinx and a number of extensions, including sphinx-jsonschema, can be found
at `Extended Sphinx <https://hub.docker.com/r/lnoor/sphinx-extended>`_.
This Docker image is generated from the Dockerfile on `Github <https://github.com/lnoor/docker-sphinx-extended>`_.

