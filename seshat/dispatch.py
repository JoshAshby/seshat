#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main framework app

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import gevent
import logging

from route_table import urls as route_table
from request import BaseRequest

logger = logging.getLogger("seshat.dispatch")

request_obj = BaseRequest
controller_folder = ""


def dispatch(env, start_response):
    """
    WSGI dispatcher

    Start off by making the global request object that gets passed around from
    this dispatcher to the controllers to the templater, the request object
    contains all the base logic to pull out the URL request parameters, build
    the session and gather the configuration bucket. It also contains logic for
    building the final header that is returned to the browser when a request is
    finished.

    After this request object has been initialized, we then go through and try
    to find a match in the global urls dictionary which contains key values of
    the regex as the key and the object to route a match on that regex to as
    the value. From there it's either processing and returning the data from
    that controller object or it's returning a 404 or 500 error page.
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
        content, head = route_table.error("404", req)
        header = head.generate_header(req, len(content))
        start_response(head.status, header)
        log_response(req, head)
        return [str(content)]

def reply(newHTTPObject, req, start_response):
    dataThread = gevent.spawn(newHTTPObject._build)
    dataThread.join()

    content, head = dataThread.get()

    if route_table.check_head(head):
        content, head = route_table.error(head, req)

    header = head.generate_header(req, len(content))

    start_response(head.status, header)

    log_response(req, head)

    gevent.spawn(req.log, head)

    return [str(content)]

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
    logger.debug("""\n\r--------- Response ---------------------
    URL: %s
    Status: %s
    """ % (req.url.path, head.status))
