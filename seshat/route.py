#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
routing decorator

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import route_table as u
from route_containers import AutoRouteContainer

import logging
logger = logging.getLogger("seshat.route")


def route():
    """
    Class decorator that will take and generate a route table entry for the
    decorated controller class, based off of its name and its file hierarchy

    Use like so::

        from seshat.controller import BaseController
        from seshat.route import route

        @route()
        class index(BaseController):
            pass

    which will result in a route for "/" being made for this controller.

    controllers whose name is `index` automatically get routed to the root of
    their folders, so an index controller in "profiles/" will have a route that
    looks like "/profiles"

    Controllers whose name is `view` will automatically get routed to any index
    route that has an attached ID. Eg::

        # In folder: profiles/
        class view(BaseController):
          pass

    will be routed to if the request URL is "/profiles/5" and the resulting
    id will be stored in `self.request.id`
    """
    def wrapper(HTTPObject):
        urlObject = AutoRouteContainer(HTTPObject)

        u.urls.add_route(urlObject)
        logger.debug("""Auto generated route table entry for:
        Object: %(objectName)s
        Pattern: %(url)s""" % {"url": urlObject.url, "objectName": HTTPObject.__module__ + "/" + HTTPObject.__name__})
        return HTTPObject
    return wrapper
