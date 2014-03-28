import seshat.dispatch as dispatch
import seshat.route as route
from seshat.controller import Controller

import os
from webob import Request

route.controller_folder = os.path.relpath(__file__).rsplit("/", 1)[0]


@route.route()
class index(Controller):
  def GET(self):
    return "hi"


@route.route()
class failure(Controller):
  def GET(self):
    raise Exception("This is an error")


def test_route_index():
  req = Request.blank("/")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "200 OK"
  assert res.body == "hi"


def test_404():
  req = Request.blank("/star-trek")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "404 NOT FOUND"


def test_500():
  req = Request.blank("/failure")
  res = req.get_response(dispatch.dispatch)
  assert res.status == "500 INTERNAL SERVER ERROR"
