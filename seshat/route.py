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
import re
import route_table as u

import logging
logger = logging.getLogger("seshat.route")

controller_folder = ""
"""The folder where the controllers are located in. Since the auto route
generation uses folder hierarchy, this setting allows to you to have
controllers in a single folder but not have that folder end up as the route
prefix."""

group_name_regex = re.compile(r"(?:\:([^/]+))")
replacement = r"(?P<\1>[^/]+)?"


class Route(object):
    """
    Provides a base route table entry which can either be used by itself or
    inherited from to make a custom process for making a route.

    Eg of use is the :py:class:`.AutoRouteContainer` which is used in
    conjunction with the :py:func:`.route` decocrator to automatically generate
    a route url.
    """
    controller = None
    """
    The controller object, of type :py:class:`.BaseController` which this
    route represents

    :type: :py:class:`.BaseController`
    """

    def __init__(self, controller=None, route=None):
        """
        TODO: Finish this doc

        :param url:
        :type url: str
        :param controller:
        :type controller: :py:class:`.BaseController`
        """
        self.controller = controller
        self.route = route

    @property
    def route(self):
        return self._route

    @route.setter
    def route(self, val):
        repl = group_name_regex.sub(replacement, val)
        repl = "^{}(?:/)?$".format(repl)
        self._route = re.compile(repl, flags=re.I)

    @property
    def title(self):
        if hasattr(self.controller, "title"): return self.controller.title
        else: return self.controller.__name__

    def match(self, url):
        res = self.route.search(url.path)
        if res:
            return res.groupdict()

    def __repr__(self):
        return "< Route Title: " + self.title + " Url: " + self.route.pattern + " Controller: " + self.controller.__module__ + "/" + self.controller.__name__ + " >"


def route(r=None):
    """
    Class decorator that will take and generate a route table entry for the
    decorated controller class, based off of its name and its file hierarchy

    Use like so::

        from seshat.controller import Controller
        from seshat.route import route

        @route()
        class index(Controller):
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
        if r is None:
          # Build the route url
            fullModule = HTTPObject.__module__

            if controller_folder:
                folder = controller_folder.replace("/", ".")
                if folder[-1] != ".":
                    folder = folder + "."

                pre_bits = fullModule.split(folder, 1)[1]

                bits = pre_bits.split(".")

            else:
                bits = fullModule.split(".")

            bases = []

            # Ignore the first and last parts of the module and make everything
            # lowercased so controllers can maybe be pep8 sometimes.
            for bit in bits[:len(bits)-1]:
                bases.append(bit.lower())

            route = "/"
            for base in bases:
                route += base + "/"

            # Everything lowercased. Because fuck uppercase... wait.
            name = HTTPObject.__name__.lower()

            if name == "index":
                route = route.rstrip("/")
                if not route: route = "/"
            else:
                route += name + ":id"

            logger.debug("""Auto generated route table entry for:
            Object: %(objectName)s
            Pattern: %(url)s""" % {"url": route, "objectName": HTTPObject.__module__ + "/" + HTTPObject.__name__})

        route = Route(controller=HTTPObject, route=route)
        u.urls.add(route)

        return HTTPObject
    return wrapper
