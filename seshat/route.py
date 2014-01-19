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
import dispatch

import logging
logger = logging.getLogger("seshat.route")


class AutoURL(object):
    """
    Base container and for generating and storing the url, and regex
    along with the object for the route table.
    """
    def __init__(self, pageObject):
        """
        Attempts to generate the base URL from the module name. This uses
        the file hierarchy within the controllers file to represent the URL.
        Controller files must contain the word `Controller` and the folder names
        can not. The actual name of the class within each Controller must be
        the camel case of the files, followed by the actual page name.  

        eg:
            controllers/admin/dev/buckets/bucketsController.py

            contains a class adminDevBucketsIndex which will be routed to
            `/admin/dev/buckets`
            and also a class adminDevBucketsSave which will be routed to
            `/admin/dev/buckets/save/`
        """
        fullModule = pageObject.__module__

        if dispatch.controller_folder:
            folder = dispatch.controller_folder.replace("/", ".")
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
            self.is_index = True
            self.url = self.url.rstrip("/")
            if not self.url: self.url = "/"
        else:
            self.is_index = False
            self.url += name

        self.pageObject = pageObject

    @property
    def title(self):
        if hasattr(self.pageObject, "title"): return self.pageObject.title
        else: return ""

    def __repr__(self):
        return "< URL Object, title: " + self.title + " url: " + self.url + " object: " + self.pageObject.__module__ + "/" + self.pageObject.__name__ + " >"


def route():
    """
    Class decorator that will take and generate a route table entry for the
    decorated controller class, based off of its name and its file hierarchy
    """
    def wrapper(HTTPObject):
        urlObject = AutoURL(HTTPObject)

        u.urls.append(urlObject)
        logger.debug("""Auto generated route table entry for:
        Object: %(objectName)s
        Pattern: %(url)s""" % {"url": urlObject.url, "objectName": HTTPObject.__module__ + "/" + HTTPObject.__name__})
        return HTTPObject
    return wrapper
