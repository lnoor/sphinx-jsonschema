# -*- coding: utf-8 -*-

"""
    sphinx-jsonschema
    -----------------
    
    This package adds the *jsonschema* directive to Sphinx.
    
    Using this directory you can render JSON Schema directly
    in Sphinx.
    
    :copyright: Copyright 2017, Leo Noordergraaf
    :licence: GPL v3, see LICENCE for details.
"""

import os.path
import json
import json_pointer
from collections import OrderedDict

from docutils.parsers.rst import Directive
from .wide_format import WideFormat

# TODO find out if app is accessible in some other way
_glob_app = None

class JsonSchema(Directive):
    optional_arguments = 1
    has_content = True
    
    def __init__(self, directive, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
        assert directive == 'jsonschema'
        
        self.options = options
        self.state = state
        self.lineno = lineno
        self.statemachine = state_machine

        if len(arguments) == 1:
            filename, pointer = self._splitpointer(arguments[0])
            self._load_external(filename)
            if pointer:
                self.schema = json_pointer.Pointer(pointer).get(self.schema)
        else:
            self._load_internal(content)

    def run(self):
        format = WideFormat(self.state, self.lineno, _glob_app)
        return format.transform(self.schema)

    def _load_external(self, file_or_url):
        if file_or_url.startswith('http'):
            try:
                import requests
            except ImportError:
                raise Exception("JSONSCHEMA loading from http requires requests. Try 'pip install requests'")
            text = requests.get(file_or_url)
            self.schema = json.loads(text.content)
        else:
            if not os.path.isabs(file_or_url):
                # file relative to the path of the current rst file
                dname = os.path.dirname(self.statemachine.input_lines.source(0))
                file_or_url = os.path.join(dname, file_or_url)
            with open(file_or_url) as file:
                self.schema = json.load(file, object_pairs_hook=OrderedDict)

    def _load_internal(self, text):
        if text is None or len(text) == 0:
            raise Exception("JSONSCHEMA requires either filename, http url or inline content")
        self.schema = json.loads('\n'.join(text), object_pairs_hook=OrderedDict)

    def _splitpointer(self, path):
        val = path.split('#', 1)
        if len(val) == 1:
            val.append(None)
        return val

def setup(app):
    global _glob_app
    _glob_app = app
    app.add_directive('jsonschema', JsonSchema)
    return {'version': '1.1'}
