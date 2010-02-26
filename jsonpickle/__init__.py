# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 John Paulett (john -at- paulett.org)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Python library for serializing any arbitrary object graph into JSON.
It can take almost any Python object and turn the object into JSON.
Additionally, it can reconstitute the object back into Python.

    >>> import jsonpickle
    >>> from samples import Thing

Create an object.

    >>> obj = Thing('A String')
    >>> print obj.name
    A String

Use jsonpickle to transform the object into a JSON string.

    >>> pickled = jsonpickle.encode(obj)
    >>> print pickled
    {"py/object": "samples.Thing", "name": "A String", "child": null}

Use jsonpickle to recreate a Python object from a JSON string

    >>> unpickled = jsonpickle.decode(pickled)
    >>> str(unpickled.name)
    'A String'

.. warning::

    Loading a JSON string from an untrusted source represents a potential
    security vulnerability.  jsonpickle makes no attempt to sanitize the input.

The new object has the same type and data, but essentially is now a copy of
the original.

    >>> obj == unpickled
    False
    >>> obj.name == unpickled.name
    True
    >>> type(obj) == type(unpickled)
    True

If you will never need to load (regenerate the Python class from JSON), you can
pass in the keyword unpicklable=False to prevent extra information from being
added to JSON.

    >>> oneway = jsonpickle.encode(obj, unpicklable=False)
    >>> print oneway
    {"name": "A String", "child": null}

"""
from jsonpickle import pickler
from jsonpickle import unpickler
from jsonpickle import pluginmgr


__version__ = '0.3.2'
__all__ = ('encode', 'decode')

# Initialize a JSONPluginMgr
json = pluginmgr.instance()

# Export specific JSONPluginMgr methods into the jsonpickle namespace
set_preferred_backend = json.set_preferred_backend
set_encoder_options = json.set_encoder_options
load_backend = json.load_backend
remove_backend = json.remove_backend


def encode(value,
           unpicklable=True, make_refs=True, max_depth=None, backend=None):
    """
    Return a JSON formatted representation of value, a Python object.

    The keyword argument 'unpicklable' defaults to True.
    If set to False, the output will not contain the information
    necessary to turn the JSON data back into Python objects.

    The keyword argument 'max_depth' defaults to None.
    If set to a non-negative integer then jsonpickle will not recurse
    deeper than 'max_depth' steps into the object.  Anything deeper
    than 'max_depth' is represented using a Python repr() of the object.

    >>> encode('my string')
    '"my string"'
    >>> encode(36)
    '36'

    >>> encode({'foo': True})
    '{"foo": true}'

    >>> encode({'foo': True}, max_depth=0)
    '"{\\'foo\\': True}"'

    >>> encode({'foo': True}, max_depth=1)
    '{"foo": "True"}'


    """
    return pickler.encode(value,
                          make_refs=make_refs,
                          backend=backend,
                          max_depth=max_depth,
                          unpicklable=unpicklable)


def decode(string, backend=None):
    """
    Convert a JSON string into a Python object.

    >>> str(decode('"my string"'))
    'my string'
    >>> decode('36')
    36
    """
    return unpickler.decode(string, backend=backend)
