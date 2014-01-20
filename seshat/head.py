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
    def __init__(self, status="200 OK", headers=None):
        self.headers = headers or []
        self.status = status
        self.error = None

    def set_header(self, key, value):
        self.headers  = [(str(key), str(value))]

    def add_header(self, key, value):
        self.headers.append((str(key), str(value)))

    def generate_header(self, req, length):
        for morsal in req.session_cookie:
            cookieHeader = ("Set-Cookie", ("%s=%s")%(morsal, req.session_cookie[morsal]))
            self.headers.append(cookieHeader)

        self.headers.append(("Content-Length", str(length)))
        self.headers.append(("Server", req._env["SERVER_SOFTWARE"]))
        self.headers.append(("X-Seshat-Says", "Ello!"))
        error = self.error[1] if self.error is not None else ""
        self.headers.append(("X-Error", error))

        return self.headers
