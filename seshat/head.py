#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""


class Head(object):
    """
    Gives a basic container for the headers within a request.
    """
    def __init__(self, status="200 OK", headers=None):
        """
        Makes a new `Head` object which can then be manipulated and returned to
        the client, eventually as a set a headers.

        :param status: The status code which this controller should instantiate
          to.
        :param headers: A `list` of `tuples` which should be used as the starting
          base for the headers.
        """
        self.headers = headers or []
        self.status = status
        """To change the status at anytime, you can simply just assign it a new
        value."""
        self.error = None
        """If an error was encounters then the stack trace will end up here"""

    def reset_headers(self):
        """
        Allows you to reset the headers
        """
        self.headers  = []

    def add_header(self, key, value):
        """
        Allows you to add a new header to the list

        Eg::

            add_header("location", "/")

        will result in the `tuple` ``("location", "/")`` being added to the
        list of headers to be returned.

        :param key: The header name
        :param value: The header value
        """
        self.headers.append((str(key), str(value)))

    def _generate_header(self, req, length):
        for morsal in req.session_cookie:
            cookieHeader = ("Set-Cookie", ("%s=%s")%(morsal, req.session_cookie[morsal]))
            self.headers.append(cookieHeader)

        self.headers.append(("Content-Length", str(length)))
        self.headers.append(("Server", req._env["SERVER_SOFTWARE"] if "SERVER_SOFTWARE" in req._env else "Unknown"))
        self.headers.append(("X-Seshat-Says", "Ello!"))
        error = self.error[1] if self.error is not None else ""
        self.headers.append(("X-Error", error))

        return self.headers
