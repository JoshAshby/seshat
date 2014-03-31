#!/usr/bin/env python
"""
# TODO: doc this
"""
"""
For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from response import Response


class ErrorCatcher(object):
    def __init__(self):
        self.codes_to_catch = {
            401: None,
            404: None,
            500: None
        }

    def register(self, code, controller):
        """
        Allows for custom error controllers to be registered. By default,
        Seshat will only handle 500 and 404 errors with a basic little bit of
        text, so this allows you to register a more advanced 500, 404, or which
        ever code, controller which can give more detailed information about
        the error, along with perhaps taking some sort of action. An example
        use for this would be registering a 401 controller which returns a
        login page.

        :param code: The code that the registering controller should respond
          to, eg: 401 or 404 NOT FOUND. This can be either just the number code
          or the full number and text description.
        :param controller: The controller class which will be used to respond
          to this code
        """
        self.codes_to_catch[code[:3]] = controller

    def __call__(self, res, req, ses):
        """
        :param res: A `.Response` object
        :param req: A `.Request` object
        """
        if res in self:
            return self.error(res.status, req, ses, errors=res.errors)

        return None

    def check(self, res):
        return int(res.status[:3]) in self.codes_to_catch.keys()

    def __contains__(self, res):
        return int(res.status[:3]) in self.codes_to_catch.keys()

    def error(self, code, req, ses, errors=None):
        if type(code) is str:
            code = int(code[:3])

        req.errors = errors

        if self.codes_to_catch.get(code):
            newHTTPObject = self.codes_to_catch[code](req, ses)
            res = newHTTPObject()

        else:
            res = Response("Error {}".format(code))
            res.status = code

        res.errors = errors
        return res


catcher = ErrorCatcher()
