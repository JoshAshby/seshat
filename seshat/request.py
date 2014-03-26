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

import cgi
import tempfile
import urlparse
from headers import Headers


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


class Request(object):
    """
    Represents the request from the server, and contains various information
    and utilities.
    """
    def __init__(self, env):
        self.params = {}
        self.files = {}
        self._env = env

        self.url = urlparse.urlparse(env["PATH_INFO"])
        """A `urlparse` result of the requests path"""

        self._parse_params()

        self.headers = Headers(env)

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
