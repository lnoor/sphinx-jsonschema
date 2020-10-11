
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sphinx-jsonschema',
    version='1.16.5',     # don't forget: must match __init__.py::setup() return value

    description='Sphinx extension to display JSON Schema',
    long_description=long_description,
    url='https://github.com/lnoor/sphinx-jsonschema',

    author='Leo Noordergraaf',
    author_email='leo@noordergraaf.net',

    license='GPLv3',
    platforms='any',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Documentation',
        'Topic :: Documentation :: Sphinx'
    ],

    keywords='sphinx json schema',
    packages=find_packages(),
    package_data={
        '': ['LICENSE']
    },

    install_requires=['docutils', 'requests', 'jsonpointer', 'pyyaml']
)

