#!/usr/bin/env python
"""
Seshat

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import Cookie
import base64
import re


# Thanks WebOB for this regex
accept_re = re.compile(r',\s*([^\s;,\n]+)(?:[^,]*?;\s*q=([0-9.]*))?')


def parse_cookie(env):
    """
    Parses the Cookie header into a `Cookie.SimpleCookie` object, or returns
    an empty new instance.
    """
    cookie = Cookie.SimpleCookie()
    if "HTTP_COOKIE" in env:
        try:
            cookie.load(env["HTTP_COOKIE"])
        except cookie.CookieError:
            pass

    return cookie


def parse_accept(s):
    """
    Parses an Accept header string and acts as an iterator, yielding a `tuple`
    of `(name, quality)`
    """
  # Again, thanks WebOB
    for match in accept_re.finditer(','+s):
        name = match.group(1)
        if name == 'q':
            continue
        quality = match.group(2)
        try:
            quality = max(min(float(quality), 1), 0) if quality else 1
            yield name, quality

        except ValueError:
            pass

def get_header_name(val):
    val = val.upper().replace("-", "_")
    return "_".join(["HTTP", val])


def get_normal_name(val):
    if val.startswith("HTTP_"):
        val = val[5:]

    return val.replace("_", "-").title()


class Authorization(object):
    """
    Basic little class to help represent an Authorization header. Currently
    only supports HTTP Basic Auth but support for digest auth is slated for
    later.

    This class is mostly unfinished at this time.
    """
    def __init__(self, auth_type, **kwargs):
        if auth_type.lower() == "basic":
            self._data = {"username": kwargs["username"],
                          "password": kwargs["password"]}
        if auth_type.lower() == "digest":
            pass #TODO

    @classmethod
    def parse(cls, env):
        if "HTTP_AUTHORIZATION" in env:
            auth_parts = env["HTTP_AUTHORIZATION"].split(" ")
            if len(auth_parts) > 1:
                if auth_parts[0].lower() == "basic":
                    name, passwd = base64.b64decode(auth_parts[1]).split(":")
                    auth = cls("basic", username=name, password=passwd)

                elif auth_parts[0].lower() == "digest":
                    pass #TODO: This. Maybe you should learn about HTTP digest auth...

        else:
            auth = None

        return auth


class Accept(object):
    """
    Basic class which can represent any number of the accept headers which
    commonly take on the form of: type/subtype; q=int
    """
    def __init__(self, s):
        self._data = { name: quality for name, quality in parse_accept(s) }

    def __contains__(self, val):
        if not "*/*" in self._data:
            return val in self._data

        return True

    def quality(self, item):
        if item in self:
            return self._data.get(item, None)
        else:
            return None


class RequestHeaders(object):
    """
    A basic container for all the headers in an HTTP request. Acts like a
    dictionary.

    This class is mostly unfinished at this time.
    """
    def __init__(self, env):
        self._env = env

        self.referer = None
        self.user_agent = None

        for key in env:
            if key not in ["HTTP_X_REAL_IP"] and key.startswith("HTTP_"):
                name = get_normal_name(key)
                val = env[key]
                if "Accept" in name:
                    val = Accept(val)

                elif "Cookie" in name:
                    val = parse_cookie(val)

                elif "Authorization" in name:
                    val = Authorization(val)

                setattr(self, name, val)

        # TODO: Parse this into something nice
        if not hasattr(self, "user_agent"):
            self.user_agent = "Unknown User Agent"
        """The user agent, unparsed, or the string `Unknown User Agent`"""

    def __getitem__(self, val):
        name = get_header_name(val)
        return self._env.get(name, None)


class ResponseHeaders(object):
    """
    Represents the headers which will be sent back to the client with the
    response. This acts a bit like an `list` of `tuples`.

    This class is mostly unfinished as of now.
    """
    def __init__(self):
        self._headers = []

    def append(self, key, val):
        key = key.title()
        self._headers.append((key, val))

    def __add__(self, val):
        assert isinstance(val, tuple)
        self._headers.append(val)

    def __contains__(self, val):
        for header in self._headers:
            if val in header:
                return True

        return False

    def __iter__(self):
        for header in self._headers:
            yield header
