Seshat Web Framework v1.0.0
===========================

Seshat is a toy web framework built by JoshAshby over the past few years. It's
aimed at being somewhat opinionated, and most definetly full of bad practices
but it gets the job done with running a few smaller sites.

Build status - Master:


.. image:: https://secure.travis-ci.org/JoshAshby/seshat.png?branch=master
        :target: http://travis-ci.org/JoshAshby/seshat


Build status - Dev:


.. image:: https://secure.travis-ci.org/JoshAshby/seshat.png?branch=dev
        :target: http://travis-ci.org/JoshAshby/seshat


Gittip if you like the work I do and would consider a small donation to help
fund me and this project:


.. raw:: html

    <iframe style="border: 0; margin: 0; padding: 0;"
        src="https://www.gittip.com/JoshAshby/widget.html"
        width="48pt" height="22pt"></iframe>



A Few Minor Warnings
--------------------

#. I have litterally NO clue what I am doing. Use at your own risk.
#. I'm only a second year university student, and software
   isn't even my major; I'm working towards an Electrical and Computer
   Engineering degree, so not only do I have limited time to keep this
   maintained, but I also probably won't write the best code ever.
#. This project follows the semantic versioning specs. All Minor and
   patch versions will not break the major versions API, however an bump of the
   major version signifies that backwards compatibility will most likely be
   broken.


Quick Start
===========

Getting started is fairly easy, take a look at the included `example.py`::

    from waitress import serve
    import seshat.dispatch as dispatch

    from seshat.route import route
    from seshat.controller import BaseController
    from seshat.actions import NotFound


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

This starts a full web app on port 8080 that you can navigate your browser to
`localhost <localhost:8080>`__ that will serve a basic page displaying the text
"Hello, World". Navigating to localhost:8080/wat will redirect you back to the
index, with the name now as "Wat".

Contributing
------------

All code for this can be found online at
`github <https://github.com/JoshAshby/seshat>`__.
If something is broken, or a feature is missing, please submit a pull request
or open an issue. Most things I probably won't have time to get around to
looking at too deeply, so if you want it fixed, a pull request is the way
to go. Besides that, I'm releasing this under the GPLv3 License as found in the
``LICENSE.txt`` file. Enjoy!

Doc Contents
------------

.. toctree::
   :maxdepth: 4

   controller
   route
   head
   actions
   request
   dispatch


Indices and tables
~~~~~~~~~~~~~~~~~~

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
