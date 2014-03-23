#!/usr/bin/env python
"""
TODO: Doc This
"""
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
import logging
logger = logging.getLogger("seshat.request")

import Cookie
import uuid
import cgi
import tempfile
import urlparse


def parse_bool(p):
  if p == "True" or p == "true":
      return True
  elif p == "False" or p == "false":
      return False
  else:
      # Well fuck
      return False


class FileObject(object):
    """
    Provides a File like object which supports the common file operations,
    along with providing some additional metadata which is sent from the
    client.
    """
    _template = "< FileObject @ {id} Filename: {filename} Data: {data} >"
    def __init__(self, file_obj):
        self.filename = file_obj.filename
        self.name = file_obj.name
        self.type = file_obj.type
        self.expanded_type = self.type.split("/")
        self.file = file_obj.file

        self.extension = ""
        parts = self.filename.split(".", 1)
        if len(parts) > 1:
            self.extension = parts[1]

    def read(self):
        return self.file.read()

    def readline(self):
        return self.file.readline()

    def seek(self, where):
        return self.file.seek(where)

    def readlines(self):
        return self.file.readlines()

    def auto_read(self):
        self.seek(0)
        data = self.read()
        self.seek(0)
        return data

    def __repr__(self):
      string = self._template.format(**{
          "id": id(self),
          "filename": self.filename,
          "data": len(self.auto_read())
        })
      return string


class BaseRequest(object):
    """
    Represents the request from the server, and contains various information
    and utilities. Also the place to store the session object.
    """
    cookie_name = "sid"
    """The name of the cookie"""

    def __init__(self, env):
        self.params = {}
        self.files = {}
        self._env = env

        self._raw_url = env["PATH_INFO"]
        self.url = urlparse.urlparse(env["PATH_INFO"])
        """A `urlparse` result of the requests path"""

        self._parse_params()
        self._parse_cookie()
        self._parse_auth()
        self.build_session()
        self.build_cfg()

        self.method = self._env["REQUEST_METHOD"].upper()
        """The HTTP method by which the request was made, in all caps."""

        self.remote = env["HTTP_X_REAL_IP"] if "HTTP_X_REAL_IP" in env else "Unknown IP"
        """The clients IP, otherwise `Unknown IP`"""

        self.user_agent = env["HTTP_USER_AGENT"] if "HTTP_USER_AGENT" in env else "Unknown User Agent"
        """The user agent, unparsed, or the string `Unknown User Agent`"""

        self.referer = env["HTTP_REFERER"] if "HTTP_REFERER" in env else ""
        """The referal URL if it exists, otherwise an empty string."""

        self.remote_accepts = []

        if "HTTP_ACCEPT" in env:
            r = env["HTTP_ACCEPT"].split(",")
            for bit in r:
                q = 1
                b = bit.split(";")
                if len(b) > 1:
                    c = b[1].split("=")
                    if len(c) > 1:
                        q = float(c[1].strip(" "))
                self.remote_accepts.append((b[0], q))

        self.pre_id_url = None
        self.id = None
        self.command = None

    def accepts(self, t):
        """
        Determines if the given mimetype is accepted by the client.
        """
        a = [ i for i in self.remote_accepts if t in i[0] ]
        return len(a) > 0

    def _post_route(self, extended):
        if extended:
            parts = extended.split('/', 1)
            self.id = parts[0]
            if len(parts) > 1:
                self.command = parts[1]
            else:
                self.command = None

        if self.id:
            self.pre_id_url = self.url.path.split(self.id)[0].strip("/").split("/")
        else:
            self.pre_id_url = self.url.path.strip("/").split("/")

    def _parse_params(self):
        all_mem = {}
        all_files = {}

        temp_file = tempfile.TemporaryFile()
        temp_file.write(self._env['wsgi.input'].read()) # or use buffered read()
        temp_file.seek(0)
        form = cgi.FieldStorage(fp=temp_file, environ=self._env, keep_blank_values=True)

        if isinstance(form.value, list):
            for bit in form:
                if hasattr(form[bit], "filename") and form[bit].filename is not None:
                    fi = FileObject(form[bit])
                    all_files[fi.name] = fi
                else:
                    all_mem[bit] = form.getvalue(bit)

        temp_file.close()

        self.params = all_mem
        self.files = all_files

    def _parse_cookie(self):
        cookie = Cookie.SimpleCookie()
        try:
            cookie.load(self._env["HTTP_COOKIE"])
            self.session_cookie = { value.key: value.value for key, value in cookie.iteritems() }
            self.session_ID = self.session_cookie[self.cookie_name]

        except Exception:
            self.session_ID = str(uuid.uuid4())
            self.session_cookie = {self.cookie_name: self.session_ID}

    def _parse_auth(self):
        if "HTTP_AUTHORIZATION" in self._env:
            auth_parts = self._env["HTTP_AUTHORIZATION"].split(" ")
            if len(auth_parts) > 1:
                if auth_parts[0].lower() == "basic":
                    name, passwd = base64.b64decode(auth_parts[1]).split(":")
                    self.auth = {"username": name, "password": passwd}
        else:
            self.auth = None

    def get_param(self, parameter, default="", cast=str):
        """
        Allows you to get a parameter from the request. If the parameter does
        not exist, or is empty, then a default will be returned. You can also
        choose to optionally cast the parameter.

        If a parameter has multiple values then this will return a list of all
        those values.

        :param parameter: The name of the parameter to get
        :param default: The default to return if the parameter is nonexistent
          or empty
        :param cast: An optional cast for the parameter.
        """
        try:
            p = self.params[parameter]
            if type(default) == bool:
                    p = parse_bool(p)

            elif cast and cast is not str:
                if cast is bool:
                    p = parse_bool(p)

                else:
                    p = cast(p)

            return p
        except:
            return default

    def get_file(self, name):
        """
        Along with getting parameters, one may wish to retrieve other data such
        as files sent.

        This provides an interface for getting a file like
        :py:class:`.FileObject` which can be used like a normal file but also
        holds some meta data sent with the request. If no file by the given
        name is found then this will return `None`
        """
        if name in self.files and self.files[name].filename:
              return self.files[name]

        else:
            return None

    @property
    def id_extended(self):
        if self.command is None:
            return str(self.id)

        else:
            return "/".join([self.id, self.command])

    def build_session(self):
        """
        Called during the objects instantiation.
        Override to set the requests `session` property.
        """
        pass

    def build_cfg(self):
        """
        Called during the objects instantiation.
        Override to set the requests `cfg` property.
        """
        pass

    def log(self, head):
        """
        Called right at the end of the request when the response is being
        returned to the client. This is useful for logging to a database or log
        file.

        :param head: The reponses :py:class:`.Head` object which was returned
          to the client.
        """
        pass
