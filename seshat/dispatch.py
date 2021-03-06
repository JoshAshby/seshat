#!/usr/bin/env python
"""
Dispatch is the actual WSGI app which is served. This module also contains
several configuration properties, along with easy access to the apps route
table though `route_table`. Documentation on the route table can be found
below: :py:class:`.RouteTable`


.. note::

    If you would like to see the logs that seshat produces, using the standard
    library `logging` module, create a handler for `seshat`
"""
"""
For more information and licensing, see: https://github.com/JoshAshby/seshat

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from greenlet import greenlet
import logging

from actions import BaseAction
from error_catcher import catcher as error_catcher
from route_table import urls as route_table
from request import BaseRequest

logger = logging.getLogger("seshat.dispatch")

request_obj = BaseRequest
"""The object which should be used to create a new Request item from. Should
inherit from BaseRequest"""


def dispatch(env, start_response):
    """
    WSGI dispatcher

    This represents the main WSGI app for Seshat.
    To use with `waitress`, for example::

        from waitress import serve
        serve(dispatch)

    """
    req = request_obj(env)
    newHTTPObject = None

    log_request(req)

    found = route_table.get(req)

    if found is not None:
        obj = found.__module__+"/"+found.__name__
        newHTTPObject = found(req)
        log_obj(req, obj)
        return reply(newHTTPObject, req, start_response)

    else:
        content, head = error_catcher.error("404", req)
        header = head._generate_header(req, len(content))
        start_response(head.status, header)
        log_response(req, head)
        return [content.encode("utf-8")]


def reply(newHTTPObject, req, start_response):
    newHTTPObj = greenlet(newHTTPObject._build)
    content, head = newHTTPObj.switch()

    if error_catcher.check(head):
        content, head = error_catcher.error(head, req)

    header = head._generate_header(req, len(content))

    start_response(head.status, header)

    log_response(req, head)

    g = greenlet(req.log)
    g.switch(head)

    return [content.encode("utf-8")]


def log_request(req):
    logger.debug("""\n\r------- Request ---------------------
    Method: %s
    URL: %s
    PARAMS: %s
    FILES: %s
    IP: %s
    UA: %s
    R: %s
    """ % (req.method, req.url.path, req.params, req.files, req.remote, req.user_agent, req.referer))


def log_obj(req, obj):
    logger.debug("""\n\r------- Processing ------------------
    Method: %s
    URL: %s
    Object: %s
    """ % (req.method, req.url.path, obj))


def log_response(req, head):
    errors = ", ".join([ str(e) for e in head.errors ])
    logger.debug("""\n\r--------- Response ---------------------
    URL: %s
    Status: %s
    Error: %s
    """ % (req.url.path, head.status, errors))
