:mod:`route`
------------

Along with needing to have controllers, an app also has to have routes to those
controllers. This is accomplished through the :py:func:`.route()`
decorator. This decorator will, if no arguments are supplied, use
:py:data:`.controller_folder` and the file hierarchy of the controller to auto
generate a route. Or you can optionally supply a custom url pattern. This
pattern then gets converted to a `dict` when the url is matched. The structure
of the url pattern is simple, variabled within the url are denoted by a colon.
For example, in the pattern::

    /user/:name/:email

the returned `dict` will be::

    {"name": something,
     "email": something_else}


.. autodata:: seshat.route.controller_folder

.. autofunction:: seshat.route.route

.. autoclass:: seshat.route.Route
    :members:

.. autoclass:: seshat.route_table.RouteTable
    :members: add, get
