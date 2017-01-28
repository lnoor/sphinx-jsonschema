# -*- coding: utf-8 -*-

"""
    WideFormat layout engine
    ------------------------
    
    In this layout for each nesting level the table is extended by
    one or more columns.
    
    :copyright: Copyright 2017, Leo Noordergraaf
    :licence: GPL v3, see LICENCE for details.
"""

from docutils import statemachine

class WideFormat:
    """Formatter varying width
    
    This formatter extends the table for each nesting level.
    """
    
    KV_SIMPLE = [
        'multipleOf', 'maximum', 'exclusiveMaximum', 'minimum', 
        'exclusiveMinimum', 'maxLength', 'minLength', 'pattern',
        'default', 'format']
    """Simple key-value pairs used in simple type definitions."""
    
    KV_ARRAY  = ['maxItems', 'minItems', 'uniqueItems']
    """Key-value pairs used in array type definitions."""
    
    KV_OBJECT = ['maxProperties', 'minProperties']
    """Key-value pairs used in object type definitions."""
    
    COMBINATORS = ['allOf', 'anyOf', 'oneOf']
    """Combinators let you select from an array of schemas."""
    
    SINGLEOBJECTS = ['not']
    """Expect a single object parameter."""
    
    def transform(self, schema, lineno = 0):
        """Main entry point.
        
        The :py:`transform` function is called to convert the schema.
        
        :param:`schema`: The schema to convert to a table.
        :param:`lineno`: The line number of the directive in the rst file.
        :returns: A complex type describing the layout and contents of the table.
        """
        self.lineno = lineno
        body = self._dispatch(schema)
        return self._cover(schema, body)

    def _dispatch(self, schema, label=None):
        # Main driver of the recursive schema traversal.
        rows = []

        if 'type' in schema:
            # select processor for type
            if schema['type'] == 'object':
                rows = self._objecttype(schema)
            elif schema['type'] == 'array':
                rows = self._arraytype(schema)
            else:
                rows = self._simpletype(schema)

        for k in self.COMBINATORS:
            # combinators belong at this level as alternative to type
            if k in schema:
                items = []
                for s in schema[k]:
                    items.append(self._dispatch(s, self._cell('-')))
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
        
        return rows

    def _cover(self, schema, body):
        # Patch up and finish the table.
        head = []
        
        # Outermost title becomes table head
        if 'title' in schema:
            head.append(self._line(self._cell(schema['title'])))
        
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
        
        if 'description' in schema:
            rows.append(self._line(self._cell(schema['description'])))
            
        if 'type' in schema:
            rows.append(
                self._line(
                    self._cell('type'), 
                    self._decodetype(schema['type'])
                )
            )

        if 'enum' in schema:
            rows.append(
                self._line(
                    self._cell('enum'),
                    self._cell(', '.join([str(e) for e in schema['enum']]))
                )
            )
        
        rows.extend(self._kvpairs(schema, self.KV_SIMPLE))
        return rows


    def _objectproperties(self, schema, key):
        # process the `properties` key of the object type
        # used for `properties`, `patternProperties` and
        # `definitions`.
        rows = []
        
        if key in schema:
            rows.append(self._line(self._cell(key)))
            
            for prop in sorted(schema[key].keys()):
                bold = ''
                if 'required' in schema:
                    if prop in schema['required']:
                        bold = '**'
                label = self._cell('- '+bold+prop+bold)
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
