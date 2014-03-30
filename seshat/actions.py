#!/usr/bin/env python
"""
Actions allow you to write code that looks like::

    class RandomController(Controller):
      def GET(self):
        return Redirect("/")

This module provides a few common Action classes to use, along with a base
Action class which can be inherited to create your own Actions by overriding
the `__init__` function.
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

    All returned data is checked if it is of type :py:class:`.Action` and if so, the
    data/actions head is returned rather than the controllers head. This allows
    for a syntax like::

        return NotFound()

    which will cause the controller to return a 404 status code.

    To create a new action, inherit this class then make a new `__init__(self, *kargs)`
    which sets `self.response` to a :py:class:`.Reponse` object (or just call
    super), and adds any headers or status changes to that :py:class:`.Response` object.
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
    """Returns a 400 BAD REQUEST"""
    def __init__(self):
        self.response = Response()
        self.response.status = 400


class Unauthorized(Action):
    """
    Returns a 401 UNAUTHORIZED back to the client

    This should probably also include a WWW-Authenticate header, but I'll leave
    that for later right now.
    """
    def __init__(self):
        self.response = Response()
        self.response.status = 401


class Forbidden(Action):
    """Returns a 403 FORBIDDEN"""
    def __init__(self):
        self.response = Response()
        self.response.status = 403


class NotFound(Action):
    """Returns a 404 Not Found"""
    def __init__(self):
        self.response = Response()
        self.response.status = 404


class MethodNotAllowed(Action):
    """
    Returns a 405 METHOD NOT ALLOWED

    :param allow: A `list` of allowable methods
    :type allow: list
    """
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
    """
    Returns a 500 INTERNAL SERVER ERROR

    :param e: The Exception
    :type e: Exception

    :param tb: The traceback of the exception
    :type tb: str
    """
    def __init__(self, e=None, tb=None):
        self.response = Response()
        self.response.status = 500
        self.response.errors = (e, tb)
