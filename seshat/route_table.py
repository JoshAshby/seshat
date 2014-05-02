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

class RouteTable(object):
    def __init__(self):
        self.routes = []

    def add(self, container):
        """
        Adds the given route container to the route table.

        :param r_container: The route container which contains the url and controller for a route.
        :type r_container: :py:class:`.Route`
        """
        self.routes.append(container)

    def get(self, request):
        """
        Attempts to find the closest match to the given url, through comparing
        lots of regexs for a match against the url.

        :param request: The requested url
        :type request: `urlparse.ParseResult`
        :return: :py:class:`.Controller` or `None`
        """
        parsed_url = request.url
        obj = None

        for container in self.routes:
            res = container.match(parsed_url)
            if res is not None:
                obj = container.controller
                request.url_params = res

                if not container.controller.__name__ == "view":
                    break

        return obj

    def __repr__(self):
        routes = ""
        routes_template = "\t{key}:\n\t\t{value}\n"
        for route in self.routes:
            route = routes_template.format(key=route.route.pattern, value=route.controller)
            routes = ''.join([routes, route])

        string = "< RouteTable @ {id} Table:\n{table}\n >"
        string = string.format(id=id(self), table=routes)

        return string


urls = RouteTable()
