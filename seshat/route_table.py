#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
route table

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import gevent
from head import Head


class RouteTable(object):
    def __init__(self):
        self._data = {}
        self.codes_to_catch = {
            "404": None,
            "500": None
            }

    def append(self, url):
        self._data[url.url] = url

    def get(self, request):
        """
        Attempts to find the closest match to the given url.
        Its messy but it gets the job done. mostly well. not sure on
        the amount of processing time it has or hasn't saved however,
        but it doesn't use regex... :/

        :parsed_url: urlparse.ParseResult
        """
        parsed_url = request.url
        obj = None
        extended = ""
        base = None
        orig_path = parsed_url.path.rstrip("/")
        if not orig_path:
            base = "/"

        else:
            if orig_path in self._data:
                base = orig_path

            else:
                found = False
                path = orig_path
                while not found:
                    path_parts = path.rsplit("/", 1)
                    base = path_parts[0]
                    if base in self._data:
                        found = True
                        extended = orig_path[len(base)+1:]

                    else:
                        path = path_parts[0]
                        if not path:
                            base = None
                            found = True

        if base is not None:
            request.post_route(extended)

            name = base

            if request.command:
                tmp = "/".join([base, request.command])
                if tmp in self._data:
                    name = tmp
            elif request.id:
                tmp = "/".join([base, "view"])
                if tmp in self._data:
                    name = tmp

            obj = self._data[name].pageObject

        return obj

    def __repr__(self):
        routes = ""
        routes_template = "\t{key}:\n\t\t{value}\n"
        for route in self._data:
            route = routes_template.format(key=route, value=self._data[route])
            routes = ''.join([routes, route])

        string = "< RouteTable @ {id} Table:\n{table}\n >"
        string = string.format(**{
            "id": id(self),
            "table": routes
          })

        return string

    def register_error(self, code, controller):
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

    def check_head(self, head):
        return head.status[:3] in self.codes_to_catch.keys()

    def error(self, head, req):
      if type(head) is not str:
          code = head.status
          error = head.error

      else:
          error = code = head

      if self.codes_to_catch[code[:3]]:
          newHTTPObject = self.codes_to_catch[code[:3]](req)
          newHTTPObject._error = error
          dataThread = gevent.spawn(newHTTPObject._build)
          dataThread.join()

          return dataThread.get()

      else:
          return "Error {}".format(code), Head(code)


urls = RouteTable()
