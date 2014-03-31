#!/usr/bin/env python
"""
Base Session class which should be used to inistantiate a new session object
which is handed off to the controllers during dispatch.
"""
"""
For more information and licensing, see: https://github.com/JoshAshby/seshat

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""


class Session(object):
    def __init__(self, request=None):
        self.request = request

        self.load()

    def load(self):
        pass

    def save(self):
        pass
