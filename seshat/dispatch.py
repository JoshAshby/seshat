#!/usr/bin/env python
"""
Dispatch is the actual WSGI app which is served. This module also contains
several configuration properties, along with easy access to the apps route
table (:py:class:`.RouteTable`) though `route_table`.

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

from error_catcher import catcher as error_catcher
from route_table import urls as route_table
from request import Request
from session import Session

logger = logging.getLogger("seshat.dispatch")

request_obj = Request
"""The class which should be used to create a new :py:class:`.Request` object from.
Should inherit from :py:class:`.Request`"""


session_obj = Session
"""The class which should be used to instantiate a new session object which
will be handed to the controller. Should at least inherit from :py:class:`.Session`"""


def dispatch(env, start_response):
    """
    WSGI dispatcher

    This represents the main WSGI app for Seshat.
    To use with `waitress`, for example::

        from waitress import serve
        serve(dispatch)

    """
    newHTTPObject = None

    req = request_obj(env)
    ses = session_obj(req)

    log_request(req)

    found = route_table.get(req)
    if found is not None:
        log_controller(req, found)

        newHTTPObject = found(request=req, session=ses)
        newHTTPObject = greenlet(newHTTPObject)

        res = newHTTPObject.switch()
        res = error_catcher(res, req, ses) or res

        ses.save()

        res.headers.append("content-length", len(res))

        log_response(req, res)

        start_response(res.status, res.headers)
        yield res.body.encode("utf-8")

    else:
        res = error_catcher.error(404, req, ses)

        start_response(res.status, res.headers)
        yield res.body.encode("utf-8")


def log_request(req):
    logger.debug("""\n\r------- Request ---------------------
    Method: %s
    URL: %s
    PARAMS: %s
    FILES: %s
    IP: %s
    UA: %s
    R: %s
    """ % (req.method, req.url.path, req.params, req.files, req.remote, req.headers.user_agent, req.headers.referer))


def log_controller(req, obj):
    logger.debug("""\n\r------- Processing ------------------
    Method: %s
    URL: %s
    Object: %s
    """ % (req.method, req.url.path, obj.__module__+"/"+obj.__name__))


def log_response(req, res):
    logger.debug("""\n\r--------- Response ---------------------
    URL: %s
    Status: %s
    Error: %s
    """ % (req.url.path, res.status, res.errors))
