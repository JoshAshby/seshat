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
import logging
logger = logging.getLogger("seshat.route")

controller_folder = ""


class RouteContainer(object):
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
    url = None
    """
    The actual url pattern for which this route is for.
    :type: `str`
    """

    def __init__(self, url, controller):
        """
        TODO: Finish this doc

        :param url:
        :type url: str
        :param controller:
        :type controller: :py:class:`.BaseController`
        """
        self.controller = controller
        self.url = url

    @property
    def title(self):
        if hasattr(self.controller, "title"): return self.controller.title
        else: return "No Title"

    def __repr__(self):
        return "< URL Object, title: " + self.title + " url: " + self.url + " object: " + self.controller.__module__ + "/" + self.controller.__name__ + " >"


class AutoRouteContainer(RouteContainer):
    def __init__(self, pageObject):
        """
        Attempts to generate the base URL from the module name. This uses
        the file hierarchy within the controllers file to represent the URL.
        """
        fullModule = pageObject.__module__

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

        self.url = "/"
        for base in bases:
            self.url += base + "/"

        # Everything lowercased. Because fuck uppercase... wait.
        name = pageObject.__name__.lower()

        if name == "index":
            self.url = self.url.rstrip("/")
            if not self.url: self.url = "/"
        else:
            self.url += name

        self.controller = pageObject
