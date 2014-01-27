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
    cookie_name = "sid"

    def __init__(self, env):
        self.params = {}
        self.files = {}
        self._env = env

        self._raw_url = env["PATH_INFO"]
        self.url = urlparse.urlparse(env["PATH_INFO"])

        self.parse_params()
        self.parse_cookie()
        self.build_session()
        self.build_cfg()

        self.method = self._env["REQUEST_METHOD"]
        self.remote = env["HTTP_X_REAL_IP"] if "HTTP_X_REAL_IP" in env else "Unknown IP"
        self.user_agent = env["HTTP_USER_AGENT"] if "HTTP_USER_AGENT" in env else "Unknown User Agent"
        self.referer = env["HTTP_REFERER"] if "HTTP_REFERER" in env else "No Referer"

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
        a = [ i for i in self.remote_accepts if t in i[0] ]
        return len(a) > 0

    def post_route(self, extended):
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

    def parse_params(self):
        all_mem = {}
        all_raw = {}
        all_files = {}

        temp_file = tempfile.TemporaryFile()
        temp_file.write(self._env['wsgi.input'].read()) # or use buffered read()
        temp_file.seek(0)
        form = cgi.FieldStorage(fp=temp_file, environ=self._env, keep_blank_values=True)

        for bit in form:
            if hasattr(form[bit], "filename") and form[bit].filename is not None:
                fi = FileObject(form[bit])
                all_files[fi.name] = fi
            else:
                all_mem[bit] = form.getvalue(bit)
                all_raw[bit] = form.getvalue(bit)

        temp_file.close()

        self.params = all_mem
        self.files = all_files

    def parse_cookie(self):
        cookie = Cookie.SimpleCookie()
        try:
            cookie.load(self._env["HTTP_COOKIE"])
            self.session_cookie = { value.key: value.value for key, value in cookie.iteritems() }
            self.session_ID = self.session_cookie[self.cookie_name]

        except Exception as e:
            logger.error(e)
            self.session_ID = str(uuid.uuid4())
            self.session_cookie = {self.cookie_name: self.session_ID}

    def get_param(self, param, default="", cast=str):
        try:
            p = self.params[param]
            if cast and cast is not str:
                if cast is bool or type(default) is bool:
                    p = parse_bool(p)
                else:
                    p = cast(p)

            return p
        except:
            return default

    def get_file(self, name):
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
        pass

    def build_cfg(self):
        pass

    def log(self, head):
        pass
