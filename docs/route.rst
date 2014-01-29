Routing
-------
Along with needing to have controllers, an app also has to have routes to those
controllers. There is a provided auto route function, described below, that
will generate the route pattern based off of the file hierarchy of where the
controller which is decorated is located at. If you prefer to make your own
routes, then you can use the described :py:class:`.RouteContainer` along with
the route tables `add_route()` to make your own routes.

.. autodata:: seshat.route_containers.controller_folder

.. autofunction:: seshat.route.route

.. autoclass:: seshat.route_containers.RouteContainer
    :members:
