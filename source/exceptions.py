# -*- coding: utf-8 -*-


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class UnrecognizedAgentNameFormat(Error):
    pass


class ConnectionError(Error):
    pass


class NoDataError(Error):
    pass
