"""Module with utils for parser"""


class NoTokenError(ValueError):
    """Is raised when string is not similar to any token"""

    pass


class InvalidSyntax(ValueError):
    """Is raised when string uses bad syntax"""

    pass
