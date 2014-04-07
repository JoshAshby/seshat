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
from cookies import Cookie, Cookies
import base64
import re

# Thanks WebOB for this regex
accept_re = re.compile(r',\s*([^\s;,\n]+)(?:[^,]*?;\s*q=([0-9.]*))?')


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
    def parse(cls, s):
        auth_parts = s.split(" ")
        if len(auth_parts) > 1:
            if auth_parts[0].lower() == "basic":
                name, passwd = base64.b64decode(auth_parts[1]).split(":")
                auth = cls("basic", username=name, password=passwd)

            elif auth_parts[0].lower() == "digest":
                pass #TODO: This. Maybe you should learn about HTTP digest auth...

        return auth

    @property
    def username(self):
        return self._data["username"]

    @property
    def password(self):
        return self._data["password"]


class Accept(object):
    """
    Basic class which can represent any number of the accept headers which
    commonly take on the form of: type/subtype; q=int
    """
    def __init__(self, s):
      # Again, thanks WebOB
        for match in accept_re.finditer(','+s):
            name = match.group(1)
            if name == 'q':
                continue
            quality = match.group(2)
            try:
                quality = max(min(float(quality), 1), 0) if quality else 1
                self._data[name] = quality

            except ValueError:
                pass

    def __contains__(self, val):
        if not "*/*" in self._data:
            return val in self._data

        return True

    def best(self, l):
        """
        Determines which item in the provided list is the best match.

        If no match is found then it'll return `None`

        :param l: A list of strings which are various accept types.
        :type l: `list`
        """
        b = (None, 0)
        for i in l:
            if i in self:
                q = self._data[i]
                if q > b[1]:
                    b = (i, q)

        return b[0]

    def quality(self, item):
        """
        Returns the quality of the given accept item, if it exists in the
        accept header, otherwise it will return `None`.
        """
        if item in self:
            return self._data.get(item, None)
        else:
            return None


class RequestHeaders(object):
    """
    A basic container for all the headers in an HTTP request. Acts like a
    dictionary.
    """
    def __init__(self, env=None):
        self.env = env or {}

        self.referer = self.referrer = self.get("referer") or self.get("referrer")
        """
        The referrer address which this request originated from.
        If no referrer is present this will return `None`
        """
        self.user_agent = self.get("user-agent") or "Unknown User Agent"
        """
        The user agent, unparsed, or the string `Unknown User Agent`

        .. note:: This will probably change to a parsed result class later on.
        """

        val = get_header_name("Authorization")
        self.authorization = Authorization(self[val]) if val in self else None
        """
        Returns an :py:class:`.Authorization` instance if there is an Authorization
        header in the request. Otherwise this returns `None`
        """

        val = get_header_name("Cookie")
        if val in self:
            self.cookies = Cookies.from_request(self[val])
        else:
            self.cookies = Cookies()

        val = get_header_name("Accept")
        self.accept = Accept(self[val]) if val in self else None

        val = get_header_name("Accept-Charset")
        self.accept_charset = Accept(self[val]) if val in self else None

        val = get_header_name("Accept-Encoding")
        self.accept_encoding = Accept(self[val]) if val in self else None

        val = get_header_name("Accept-Language")
        self.accept_language = Accept(self[val]) if val in self else None

    def get(self, val, default=None):
        if not val.startswith("HTTP_"):
            val = get_header_name(val)

        return self.env.get(val, default)

    def __getitem__(self, val):
        if not val.startswith("HTTP_"):
            val = get_header_name(val)

        return self.env[val]

    def __contains__(self, val):
        if not val.startswith("HTTP_"):
            val = get_header_name(val)

        return val in self.env


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
