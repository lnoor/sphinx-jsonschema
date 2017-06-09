# -*- coding: utf-8 -*-

"""
    WideFormat layout engine
    ------------------------
    
    In this layout for each nesting level the table is extended by
    one or more columns.
    
    :copyright: Copyright 2017, Leo Noordergraaf
    :licence: GPL v3, see LICENCE for details.
"""

import string
from docutils import statemachine
from docutils import nodes
from docutils.nodes import fully_normalize_name as normalize_name

class WideFormat(object):
    
    KV_SIMPLE = [
        'multipleOf', 'maximum', 'exclusiveMaximum', 'minimum', 
        'exclusiveMinimum', 'maxLength', 'minLength', 'pattern',
        'default', 'format']
    
    KV_ARRAY  = ['maxItems', 'minItems', 'uniqueItems']
    
    KV_OBJECT = ['maxProperties', 'minProperties']
    
    COMBINATORS = ['allOf', 'anyOf', 'oneOf']
    
    SINGLEOBJECTS = ['not']
    
    def __init__(self, state, lineno, app):
        super(WideFormat, self).__init__()
        self.app = app
        self.trans = None
        self.lineno = lineno
        self.state = state
        self.nesting = 0
        
    def transform(self, schema):
        body = self._dispatch(schema)
        cols, head, body = self._cover(schema, body)
        table = self.state.build_table((cols, head, body), self.lineno)
        return self._wrap_in_section(schema, table)
        

    def _dispatch(self, schema, label=None):
        # Main driver of the recursive schema traversal.
        rows = []
        self.nesting += 1

        if 'type' in schema:
            # select processor for type
            if schema['type'] == 'object':
                rows = self._objecttype(schema)
            elif schema['type'] == 'array':
                rows = self._arraytype(schema)
            else:
                rows = self._simpletype(schema)

        if '$ref' in schema:
            rows.append(self._line(self._cell(':ref:`'+schema['$ref']+'`')))

        for k in self.COMBINATORS:
            # combinators belong at this level as alternative to type
            if k in schema:
                items = []
                for s in schema[k]:
                    items.extend(self._dispatch(s, self._cell('-')))
                rows.extend(self._prepend(self._cell(k), items))

        for k in self.SINGLEOBJECTS:
            # combinators belong at this level as alternative to type
            if k in schema:
                rows.extend(self._dispatch(schema[k], self._cell(k)))

        # definitions aren't really type equiv's but still best place for them
        rows.extend(self._objectproperties(schema, 'definitions'))

        if label is not None:
            # prepend label column if required
            rows = self._prepend(label, rows)
        
        self.nesting -= 1
        return rows


    def _cover(self, schema, body):
        # Patch up and finish the table.
        head = []
        
        # Outermost id becomes schema url
        # NB: disregards interior id's
        if 'id' in schema:
            body.insert(0, self._line(self._cell(schema['id'])))
        
        # patch up if necessary, all rows should be of equal length
        nrcols = self._square(body)
        # assume len(head[n]) <= nrcols
        nrcols = self._square(head, nrcols)

        # create column spans and proper type casts
        self._calc_spans(head, nrcols)
        self._calc_spans(body, nrcols)

        # All columns have same width, to change alter the first element
        return [1] * nrcols, head, body


    def _wrap_in_section(self, schema, table):
        
        result = list()
        if '$$target' in schema:
            # Wrap section and table in a target (anchor) node so
            # that it can be referenced from other sections.
            labels = self.app.env.domaindata['std']['labels']
            anonlabels = self.app.env.domaindata['std']['anonlabels']
            docname = self.app.env.docname
            targets = schema['$$target']
            if not isinstance(targets, list):
                targets = [targets]

            targetnode = nodes.target()
            for target in targets:
                anchor = normalize_name(target)
                targetnode['ids'].append(anchor)
                targetnode['names'].append(anchor)
                anonlabels[anchor] = docname, targetnode['ids'][0]
                labels[anchor] = docname, targetnode['ids'][0], (schema['title'] if 'title' in schema else anchor)
            targetnode.line = self.lineno
            result.append(targetnode)
            
        if 'title' in schema:
            # Wrap the resulting table in a section giving it a caption and an
            # entry in the table of contents.
            memo = self.state.memo
            mylevel = memo.section_level
            memo.section_level += 1
            section_node = nodes.section()
            textnodes, title_messages = self.state.inline_text(schema['title'], self.lineno)
            titlenode = nodes.title(schema['title'], '', *textnodes)
            name = normalize_name(titlenode.astext())
            section_node['names'].append(name)
            section_node += titlenode
            section_node += title_messages
            self.state.document.note_implicit_target(section_node, section_node)
            section_node += table
            memo.section_level = mylevel
            result.append(section_node)
        else:
            result.append(table)
        return result
    
    def _objecttype(self, schema):
        # create description and type rows
        rows = self._simpletype(schema)
        rows.extend(self._objectproperties(schema, 'properties'))
        rows.extend(self._objectproperties(schema, 'patternProperties'))
        rows.extend(self._bool_or_object(schema, 'additionalProperties'))
        rows.extend(self._kvpairs(schema, self.KV_OBJECT))
        return rows

    def _arraytype(self, schema):
        # create description and type rows
        rows = self._simpletype(schema)
        
        if 'items' in schema:
            # add items label
            rows.append(self._line(self._cell('items')))
            items = schema['items'] if type(schema['items']) == list else [schema['items']]
            for item in items:
                label = self._cell('-')
                rows.extend(self._dispatch(item, label))

        rows.extend(self._bool_or_object(schema, 'additionalItems'))
        rows.extend(self._kvpairs(schema, self.KV_ARRAY))
        return rows
    
    def _simpletype(self, schema):
        rows = []

        if 'title' in schema and self.nesting > 1:
            rows.append(self._line(self._cell('*'+schema['title']+'*')))
        
        if 'description' in schema:
            rows.append(self._line(self._cell(schema['description'])))
            
        if 'type' in schema:
            rows.append(self._line(self._cell('type'), self._decodetype(schema['type'])))

        if 'enum' in schema:
            rows.append(self._line(self._cell('enum'), self._cell(', '.join([str(e) for e in schema['enum']]))))
        
        rows.extend(self._kvpairs(schema, self.KV_SIMPLE))
        return rows


    def _objectproperties(self, schema, key):
        # process the `properties` key of the object type
        # used for `properties`, `patternProperties` and
        # `definitions`.
        rows = []
        
        if key in schema:
            rows.append(self._line(self._cell(key)))
            
            for prop in schema[key].keys():
                # insert spaces around the regexp OR operator
                # allowing the regexp to be split over multiple lines.
                proplist = prop.split('|')
                dispprop = ' | '.join(proplist)
                bold = ''
                if 'required' in schema:
                    if prop in schema['required']:
                        bold = '**'
                label = self._cell('- '+bold+dispprop+bold)
                obj = schema[key][prop]
                rows.extend(self._dispatch(obj, label))
        return rows
    
    def _bool_or_object(self, schema, key):
        # for those attributes that accept either a boolean or a schema.
        rows = []
        
        if key in schema:
            if type(schema[key]) == bool:
                rows.append(self._line(self._cell(key), self._cell(schema[key])))
            else:
                rows.extend(self._dispatch(schema[key], self._cell(key)))
        
        return rows

    def _kvpairs(self, schema, keys):
        # render key-value pairs
        rows = []
        
        for k in keys:
            if k in schema:
                rows.append(self._line(self._cell(k), self._cell(schema[k])))
        return rows
    
    def _prepend(self, prepend, rows):
        # prepend a label to a set of rows
        rcnt = len(rows)
        
        if rcnt == 0:
            # return a row with only the label
            return [self._line(prepend)]
        else:
            # add the label to the first row
            prepend[0] = rcnt - 1
            rows[0].insert(0, prepend)
            # following rows have an empty column prepended
            for r in range(1, rcnt):
                rows[r].insert(0, None)
            return rows
        
    def _decodetype(self, typ):
        # render (array of) simple type(s)
        if type(typ) == list:
            # construct list of basic types
            return self._cell(' / '.join(['*'+s+'*' for s in typ]))
        else:
            # create a single type
            return self._cell('*'+typ+'*')

    def _square(self, rows, nrcols = 0):
        #determine max. number of columns
        if nrcols == 0:
            for row in rows:
                nrcols = max(nrcols, len(row))
        
        # extend each row to contain same number of columns
        for row in rows:
            if len(row) < nrcols:
                row += [None] * (nrcols - len(row))
        
        return nrcols
    
    def _calc_spans(self, rows, nrcols):
        # calculate colspan
        for row in rows:
            target = None
            for c in range(nrcols):
                if row[c] is not None:
                    # try to extend colspan on this cell
                    target = row[c]
                else:
                    if target is not None:
                        # extend colspan
                        target[1] += 1
        
        # convert arrays to tuples
        # arrays are needed to patch up colspan and rowspan
        # the table builder requires each cell to be a tuple, not an array
        for row in rows:
            for c in range(nrcols):
                if row[c] is not None:
                    row[c] = tuple(row[c])

    
    def _line(self, *cells):
        # turn a number of cells into a list
        return [ c for c in cells ]
    
    def _cell(self, text):
        # Table builder wants all cells as a tuple of 4 fields.
        # Returns a list since it needs to be mutable (tuple isn't).
        # Eventually, _calc_spans() will turn these lists into tuples.
        return [
            0,              # rowspan
            0,              # colspan
            self.lineno,    # source line number

            # turn string into multiline array of views on lists
            # required by table builder
            statemachine.ViewList(statemachine.string2lines(str(text)))
        ]
