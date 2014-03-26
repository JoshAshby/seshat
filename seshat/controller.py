#!/usr/bin/env python
"""
No app built with Seshat does much without controllers. This module provides a
base controller class which can be used right away in its current state, or can
be inherited from to create more advanced or custom controllers.

Basic use is like so::

    from seshat.controller import BaseController

    class index(BaseController):
      def GET(self):
        return "<h1>WAT</h1>"

If you see something along the lines of 'Content Generating Request Method' it
will usually mean ``GET()``, ``POST()``, or any other HTTP method verb which
might be given to the controller.
"""
"""
For more information and licensing, see: https://github.com/JoshAshby/seshat

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import traceback
import actions
import logging
from response import Response

logger = logging.getLogger("seshat.controller")


class Controller(object):
    """
    The parent of all controllers which Seshat will serve.

    To use this to make a controller, override or add the request method (in
    all caps) which will be called for this controller. Eg, with the
    controller::

        from seshat.controller import BaseController

        class index(BaseController):
          def GET(self):
            return "<h1>WAT</h1>"

    then all GET method requests to this controller will return with the text
    `<h1>WAT</h1>` however all POST, PUT, DELETE calls will return as a blank
    page, since those methods are not overridden.

    .. note::

        Support for `Not Supported` status codes may be added later, ironically.
    """
    def __init__(self, request):
        self.request = request
        self.post_init_hook()

    def post_init_hook(self):
        """
        Called at the end of `__init__` this allows you to customize the
        creation process of your controller, without having to override
        `__init__ itself`.

        This should accept nothing and return nothing.
        """
        pass

    def __call__(self):
      content = None
      try:
          c = self.pre_content_hook()
          if c is not None:
              if isinstance(c, actions.BaseAction):
                  return c

          if hasattr(self, self.request.method):
              content = getattr(self, self.request.method)()
              if isinstance(content, actions.BaseAction):
                  return content

              self.post_content_hook(content)
          else:
              return actions.MethodNotSupported()

      except Exception as e:
          tb = str(traceback.format_exc())
          logger.exception(e)
          logger.error(tb)
          self.req.error = (e, tb)

      return content

    def pre_content_hook(self):
        """
        Called before the generating request method is called and should return either
        `None` or :py:class:`.Head` or :py:class:`.BaseAction` object.

        If there is a returned value other than None, this will skip calling
        the content generating request method and simply return directly to
        dispatch.

        A good example of the use for this hook would be for authentication.
        You could for example, check the id set through the cookie and compare
        it to a database entry. If the cookie is not currently in use (ie, user
        not logged in, or similar) then you could do::

            return Head("401")

        or perhaps::

            return actions.Unauthorized()

        :rtype: :py:class:`.Head` or :py:class:`.BaseAction` or `None`
        """
        return None

    def post_content_hook(self, content):
        """
        Gets called after the content generating request method has been
        called. This can be to further modify the content which is returned, or
        perform some other action after each request.

        :param content: the content from the content generating request method
          that was called.
        :type content: `str`

        :return: The original or modified content
        :rtype: `str`
        """
        return content

    def HEAD(self):
        """
        Will be called if the request method is HEAD

        By default this will call `GET()` but return nothing, so that only the
        Headers are returned to the client.
        """
        self.GET()

    def GET(self):
        """
        Will be called if the request method is GET
        """
        pass
