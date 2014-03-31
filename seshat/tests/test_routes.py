from seshat.route_table import urls as route_table
import seshat.route as route
import seshat.request as request
from seshat.controller import Controller

import os


route.controller_folder = os.path.relpath(__file__).rsplit("/", 1)[0]


@route.route()
class index(Controller):
  def GET(self):
    return "hi"

def test_route_table_index():
    req = request.Request({"PATH_INFO": "/"})
    assert route_table.get(req) is index
