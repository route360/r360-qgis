"""Error types

Custom error classes for plugin
"""


class KillError(Exception):
    """For use inside worker when killed during execution"""
    pass


class KillTimeoutError(Exception):
    """A worker couldn't stop gracefully"""
    pass


class RequestError(Exception):
    """An API request failed"""
    pass
