#!/usr/bin/env python
"""
Actions allow you to write code that looks like::

    class RandomController(Controller):
      def GET(self):
        return Redirect("/")

This module provides a few common Action classes to use, along with a
Action which can be inherited to create your own Actions.
"""
"""
For more information and licensing, see: https://github.com/JoshAshby/seshat

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from response import Response


class Action(object):
    """
    Provides a base for creating a new object which represents an HTTP Status code.

    All returned data is checked if it is of type `Action` and if so, the
    data/actions head is returned rather than the controllers head. This allows
    for a syntax like::

        return NotFound()

    which will cause the controller to return a 404 status code.

    To create a new action, inherit this class then make a new `__init__(self, *kargs)`
    which sets `self.head` to a :py:class:`.Head` object.
    """
    def __init__(self):
        self.response = Response()

    def __call__(self): return self.response


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
class Redirect(Action):
    """
    Returns a 303 See Other status code along with a `location` header back
    to the client.

    :param loc: The location to which the client should be redirect to
    :type loc: str
    """
    def __init__(self, loc):
        self.response = Response()
        self.response.status = 303
        self.response.headers.append("Location", loc)


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
class BadRequest(Action):
    def __init__(self):
        self.response = Response()
        self.response.status = 400


class Unauthorized(Action):
    """
    Returns a 401 Unauthorized status code back to the client
    """
    def __init__(self):
        self.response = Response()
        self.response.status = 401


class Forbidden(Action):
    def __init__(self):
        self.response = Response()
        self.response.status = 403


class NotFound(Action):
    """
    Returns a 404 Not Found code and the resulting 404 error controller to be
    returned to the client.
    """
    def __init__(self):
        self.response = Response()
        self.response.status = 404


class MethodNotAllowed(Action):
    def __init__(self, allow):
        self.response = Response()
        self.response.status = 405
        assert type(allow) is list
        a = ", ".join(allow).upper()
        self.response.headers.append("Allow", a)


##############################################################################
   #####     ###       ###
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
       #   ##   ##   ##   ##
    ####   ##   ##   ##   ##
   #       ##   ##   ##   ##
  #        ##   ##   ##   ##
   #       ##   ##   ##   ##
    ####     ###       ###
##############################################################################

class InternalServerError(Action):
    def __init__(self, e=None, tb=None):
        self.response = Response()
        self.response.status = 500
        self.response.errors = (e, tb)
