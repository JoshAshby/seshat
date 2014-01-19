#!/usr/bin/env python
__version__ = '1.0.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ["dispatch",
           "actions",
           "request",
           "route"]
