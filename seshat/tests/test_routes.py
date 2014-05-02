import seshat.dispatch as dispatch
from seshat.route_table import urls as route_table
import seshat.route as route
import seshat.request as request
from seshat.controller import Controller

import os
from webob import Request


route.controller_folder = os.path.relpath(__file__).rsplit("/", 1)[0]


@route.route()
class failure(Controller):
  def GET(self):
    raise Exception("This is an error")


@route.route()
class index(Controller):
  def GET(self):
    return "hi"


@route.route()
class users(Controller):
  def GET(self):
    return ""


@route.route("/users/:id")
class view_users(Controller):
    def GET(self):
        return "Hia"


@route.route("/users/:id/:email_settings")
class two_param_route(Controller):
    def GET(self):
        return "This is email?"


def test_route_table_index():
    req = request.Request({"PATH_INFO": "/"})
    print route_table.get(req)
    assert route_table.get(req) is index


def test_route_table_users():
    req = request.Request({"PATH_INFO": "/users"})
    a = route_table.get(req)
    assert a is users
    req = request.Request({"PATH_INFO": "/users/"})
    a = route_table.get(req)
    assert a is users


def test_custom_route():
    req = request.Request({"PATH_INFO": "/users/Josh"})
    a = route_table.get(req)
    assert a is view_users
    req = request.Request({"PATH_INFO": "/users/Josh/"})
    a = route_table.get(req)
    assert a is view_users


def test_two_param_route():
    req = request.Request({"PATH_INFO": "/users/Josh/true"})
    a = route_table.get(req)
    assert a is two_param_route
    req = request.Request({"PATH_INFO": "/users/Josh/true/"})
    a = route_table.get(req)
    assert a is two_param_route


def test_route_table_repr():
    route_table.__repr__()



def test_dispatch_index():
  req = Request.blank("/")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "200 OK"
  assert res.body == "hi"


def test_404_dispatch():
  req = Request.blank("/star-trek")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "404 NOT FOUND"
  req = Request.blank("/star-trek/")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "404 NOT FOUND"


def test_500_dispatch():
  print dispatch.route_table.routes
  req = Request.blank("/failure")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "500 INTERNAL SERVER ERROR"
  req = Request.blank("/failure/")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "500 INTERNAL SERVER ERROR"
