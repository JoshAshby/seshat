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
    head = None
    def __len__(self):
        return 0

    def __str__(self):
        return ""

    def __unicode__(self):
        return ""


class Redirect(BaseAction):
    def __init__(self, loc):
        self.head = Head("303 SEE OTHER")
        self.head.add_header("Location", loc)


class NotFound(BaseAction):
    def __init__(self):
        self.head = Head("404 NOT FOUND")


class Unauthorized(BaseAction):
    def __init__(self):
        self.head = Head("401 UNAUTHORIZED")
