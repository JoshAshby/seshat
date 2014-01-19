from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import seshat.dispatch as dispatch

from seshat.route import route
from seshat.base_object import BaseObject
from seshat.actions import NotFound

@route()
class index(BaseObject):
  def GET(self):
    return "wat"

@route()
class wat(BaseObject):
  def GET(self):
    return NotFound()

server = WSGIServer(("127.0.0.1", 8001), dispatch.dispatch, log=None)
server.serve_forever()
