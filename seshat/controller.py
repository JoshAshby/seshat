#!/usr/bin/env python
"""
No app built with Seshat does much without controllers. This module provides a
base controller class which can be used right away in its current state, or can
be inherited from to create more advanced or custom controllers.

Basic use is like so::

    from seshat.controller import Controller

    class index(Controller):
      def GET(self):
        return "<h1>WAT</h1>"

By default all controllers have HEAD and GET methods. HEAD simply calls GET but
strips the reponse body. (HEAD is probably broken for now but I'll fix it
eventually).

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
from headers import ResponseHeaders

logger = logging.getLogger("seshat.controller")


class Controller(object):
    """
    The parent of all controllers which Seshat will serve.

    To use this to make a controller, override or add the request method (in
    all caps) which will be called for this controller. Eg::

        from seshat.controller import Controller

        class index(Controller):
          def GET(self):
            return "<h1>WAT</h1>"

    then all GET based requests to this controller will return with the text
    `<h1>WAT</h1>` however all POST, PUT, DELETE calls will a 405 Method Not
    Supported error.
    """
    def __init__(self, request):
        self.request = request
        self.post_init_hook()
        self.headers = ResponseHeaders()

    def post_init_hook(self):
        """
        Called at the end of `__init__` this allows you to customize the
        creation process of your controller, without having to override
        `__init__` itself.

        This should accept nothing and return nothing.
        """
        pass

    def __call__(self):
      try:
          c = self.pre_content_hook()
          if c is not None:
              if isinstance(c, actions.Action):
                  return c()

          if hasattr(self, self.request.method):
              c = getattr(self, self.request.method)()

              if isinstance(c, actions.Action):
                  return c()

              self.post_content_hook(c)

              return Response(200, self.headers, c)

          else:
              return actions.MethodNotSupported()()
            # TODO: Add code to make this not crash

      except Exception as e:
          tb = str(traceback.format_exc())
          logger.exception(e)
          logger.error(tb)
          return actions.InternalServerError(e, tb)()

    def pre_content_hook(self):
        """
        Called before the request method is called and should return either
        `None` or :py:class:`.Action` object.

        If there is a returned value other than None, this will skip calling
        the request method and simply return directly to dispatch, so make sure
        it returns an :py:class:`.Action`.

        A good example of the use for this hook would be for authentication.
        You could for example, check a parameter set through a cookie and
        return something like a 401 Unauthorized if the param doesn't represent
        a logged in user::

            return actions.Unauthorized()

        :rtype: :py:class:`.Action` or `None`
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
