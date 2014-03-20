#!/usr/bin/env python
"""
Actions allow you to write code that looks like::

    class RandomController(BaseController):
      def GET(self):
        return Redirect("/")

which I think looks a lot nicer than::

    class RandomController(BaseController):
      def GET(self):
        self.head.status = "303 SEE OTHER"
        self.head.append("location", "/")

This module provides a few common Action classes to use, along with a
BaseAction which can be inherited to create your own Actions.
"""
"""
For more information and licensing, see: https://github.com/JoshAshby/seshat

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from head import Head


class BaseAction(object):
    """
    Provides a base for creating a new object which represents an HTTP Status code.

    All returned data is checked if it is of type `BaseAction` and if so, the
    data/actions head is returned rather than the controllers head. This allows
    for a syntax like::

        return NotFound()

    which will cause the controller to return a 404 status code.

    To create a new action, inherit this class then make a new `__init__(self, *kargs)`
    which sets `self.head` to a :py:class:`.Head` object.
    """
    head = None
    def __len__(self):
        return 0

    def __str__(self):
        return ""

    def __unicode__(self):
        return ""

    def encode(self, val):
        return str(self).encode(val)


##############################################################################
  ######     ###       ###
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
  ######   ##   ##   ##   ##
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
  ######     ###       ###
##############################################################################
class Redirect(BaseAction):
    """
    Returns a 303 See Other status code along with a `location` header back
    to the client.

    :param loc: The location to which the client should be redirect to
    :type loc: str
    """
    def __init__(self, loc):
        self.head = Head("303 SEE OTHER")
        self.head.add_header("Location", loc)


##############################################################################
     ###     ###       ###
    #  #   ##   ##   ##   ##
   #   #   ##   ##   ##   ##
  #    #   ##   ##   ##   ##
 #######   ##   ##   ##   ##
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
       #     ###       ###
##############################################################################
class BadRequest(BaseAction):
    def __init__(self):
        self.head = Head("400 BAD REQUEST")


class Unauthorized(BaseAction):
    """
    Returns a 401 Unauthorized status code back to the client
    """
    def __init__(self):
        self.head = Head("401 UNAUTHORIZED")


class Forbidden(BaseAction):
    def __init__(self):
        self.head = Head("403 FORBIDDEN")


class NotFound(BaseAction):
    """
    Returns a 404 Not Found code and the resulting 404 error controller to be
    returned to the client.
    """
    def __init__(self):
        self.head = Head("404 NOT FOUND")


class MethodNotAllowed(BaseAction):
    def __init__(self, allow):
        assert type(allow) is list
        a = ", ".join(allow).upper()
        al = [("Allow", a)]
        self.head = Head("405 METHOD NOT ALLOWED", al)
