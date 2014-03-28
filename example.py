from waitress import serve
import seshat.dispatch as dispatch

from seshat.route import route
from seshat.controller import Controller
from seshat.actions import Redirect


@route()
class index(Controller):
  def GET(self):
    name = self.request.get_param("name", "World!")
    return "Hello, " + name


@route()
class wat(Controller):
  def GET(self):
    return Redirect("/?name=Wat")


serve(dispatch.dispatch)
