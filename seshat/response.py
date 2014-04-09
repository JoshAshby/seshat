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
from headers import ResponseHeaders


# Thanks werkzeug
# Shamefully taken from https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/http.py#L63
lookup_codes = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi Status',
    226: 'IM Used',              # see RFC 3229
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',     # unused
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: 'I\'m a teapot',        # see RFC 2324
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',
    428: 'Precondition Required', # see RFC 6585
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    449: 'Retry With',           # proprietary MS extension
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    507: 'Insufficient Storage',
    510: 'Not Extended'
}


def get_status_code_str(num):
    s = lookup_codes.get(num, None)
    if s:
        s = s.upper()
        s = "{} {}".format(num, s)

    return s


class Response(object):
    def __init__(self, status_code=200, headers=None, body=None):
        self.status = status_code
        self.headers = ResponseHeaders(headers)
        self.body = body or ""
        self.errors = None

    def __len__(self):
        return len(self.body)

    def __repr__(self):
        return "<Response at {id} with status={status}, headers={headers}, body={body}".format(id=id(self), status=self.status, headers=self.headers, body=self.body)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        if isinstance(val, int):
            s = get_status_code_str(val)
        else:
            s = val

        self._status = s
