#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import traceback
import actions

from head import Head


class BaseObject(object):
    error = None
    """
    Base page response object
    """
    def __init__(self, request):
        self.head = Head()
        self.request = request
        self.post_init_hook()

    def post_init_hook(self):
        pass

    def _build(self):
      content = ""
      self.pre_content_hook()
      try:
          content = getattr(self, self.request.method)()
          if isinstance(content, actions.BaseAction):
              self.head = content.head

          else:
              content = unicode(content)

      except Exception:
          self.head.error = str(traceback.format_exc())

      return content, self.head

    def pre_content_hook(self):
        pass

    def post_content_hook(self):
        pass

    def HEAD(self):
        """
        This is wrong since it should only return the headers... technically...
        """
        return self.GET()

    def GET(self):
        pass

    def POST(self):
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass
