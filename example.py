from waitress import serve
import seshat.dispatch as dispatch

from seshat.route import route
from seshat.controller import BaseController
from seshat.actions import Redirect


@route()
class index(BaseController):
  def GET(self):
    name = self.request.get_param("name", "World!")
    return "Hello, " + name


@route()
class wat(BaseController):
  def GET(self):
    return Redirect("/?name=Wat")


serve(dispatch.dispatch)
