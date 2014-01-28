import seshat.dispatch as dispatch
from seshat.route import route
from seshat.controller import BaseController

import os
from webob import Request

dispatch.controller_folder = os.path.relpath(__file__).rsplit("/", 1)[0]

@route()
class index(BaseController):
  def GET(self):
    return "hi"


@route()
class failure(BaseController):
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
  assert res.body == "Error 404 NOT FOUND"
  assert res.status == "404 NOT FOUND"


def test_500():
  req = Request.blank("/failure")
  res = req.get_response(dispatch.dispatch)
  assert res.body == "Error 500 INTERNAL SERVER ERROR"
  assert res.status == "500 INTERNAL SERVER ERROR"
