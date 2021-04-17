"""Module with tokens for parser"""


class EOF:
    def __init__(self):
        pass


class CONST:
    VALUES = ['0', '1']

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_const(value: str):
        if value in CONST.VALUES:
            return True

        return False


class SYBMOL:
    VALUES = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_symbol(value: str):
        if value in SYBMOL.VALUES:
            return True

        return False


class OPEN_BRACKET:
    VALUE = '('

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_open_bracket(value: str):
        if value == OPEN_BRACKET.VALUE:
            return True

        return False


class CLOSE_BRACKET:
    VALUE = ')'

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_close_bracket(value: str):
        if value == CLOSE_BRACKET.VALUE:
            return True

        return False


class AND_OPERATOR:
    VALUE = '/\\'

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_and_operator(value: str):
        if value == AND_OPERATOR.VALUE:
            return True

        return False


class OR_OPERATOR:
    VALUE = '\\/'

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_or_operator(value: str):
        if value == OR_OPERATOR.VALUE:
            return True

        return False


class NOT_OPERATOR:
    VALUE = '!'

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_not_operator(value: str):
        if value == NOT_OPERATOR.VALUE:
            return True

        return False


class IMPLICATION:
    VALUE = '->'

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_implication(value: str):
        if value == IMPLICATION.VALUE:
            return True

        return False


class EQUIVALENCE:
    VALUE = '~'

    def __init__(self, value: str):
        self.value = value

    @staticmethod
    def is_equivalence(value: str):
        if value == EQUIVALENCE.VALUE:
            return True

        return False
