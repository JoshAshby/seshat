from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import seshat.dispatch as dispatch

from seshat.route import route
from seshat.base_object import BaseObject

@route()
class index(BaseObject):
  def GET(self):
    return "wat"

server = WSGIServer(("127.0.0.1", 8000), dispatch.dispatch, log=None)
server.serve_forever()
