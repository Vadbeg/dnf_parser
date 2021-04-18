"""Module with utils for parser"""


class NoTokenError(ValueError):
    """Is raised when string is not similar to any token"""

    pass


class InvalidSyntax(ValueError):
    """Is raised when string uses bad syntax"""

    pass


class NotSimpleConjunctionBadOperation(ValueError):
    """Is raised when leaf of tree is not simple conjunction"""

    pass


class NotSimpleConjunctionBadNot(ValueError):
    """Is raised when leaf of tree is not simple conjunction (not used not for symbol)"""

    pass


class NotSimpleConjunctionSameValues(ValueError):
    """Is raised when leaf of tree is not simple conjunction (not used not for symbol)"""

    pass


class BadTokensForDNF(ValueError):
    """Is raised when tokens are not used for DNF"""

    pass