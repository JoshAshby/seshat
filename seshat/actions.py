#!/usr/bin/env python
"""
various actions to return from an object.

For more information, see: https://github.com/JoshAshby/

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
    which sets `self.head` to a `seshat.head.Head` object.
    """
    head = None
    def __len__(self):
        return 0

    def __str__(self):
        return ""

    def __unicode__(self):
        return ""


class Redirect(BaseAction):
    """
    Causes the controller which returns this to send a 303 See Other status
    code back to the client.
    """
    def __init__(self, loc):
        """
        Sets the location of where the client should be redirected to

        :param loc: The location to which the client should be redirect to
        :type loc: str
        """
        self.head = Head("303 SEE OTHER")
        self.head.add_header("Location", loc)


class NotFound(BaseAction):
    """
    Returns a 404 Not Found code and the resulting 404 error controller to be
    returned to the client.
    """
    def __init__(self):
        self.head = Head("404 NOT FOUND")


class Unauthorized(BaseAction):
    """
    Returns a 401 Unauthorized status code back to the client
    """
    def __init__(self):
        self.head = Head("401 UNAUTHORIZED")
