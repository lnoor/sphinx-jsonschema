
Orginization
============

As stated earlier, I needed this to manage and document rather large schemas.
I wanted to organize these schemas in such a way that the number of levels
remained under control. Have a look at the documentation and schemas at the
`Nextpertise API documentation <http://api.nextpertise.nl/documentation>`_ for
an example.

To achieve this I wanted the schemas to be able to reference other (reusable) schemas
using the ``$ref`` keyword. These subschemas, should be documented somewhere else but
should be all in a single file for performance reasons.

So in order to separate storage and representation I require each ``$ref``-erenced subschema
to be included explicitly in your .rst file.
