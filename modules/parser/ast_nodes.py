"""Module with nodes for ast (abstract-syntax trees)"""


from typing import Union, Optional

from modules.tokens import TOKEN, CONST, SYBMOL, NOT_OPERATOR


class AST:
    pass


class Value(AST):
    def __init__(self, token: Union[CONST, SYBMOL]):
        self.token = token
        self.value = token.value


class BinOp(AST):
    def __init__(
            self, left: Optional[Union['BinOp', Value]],
            operation: TOKEN,
            right: Optional[Union['BinOp', Value]]
    ):
        self.left = left
        self.operation = operation
        self.right = right


class NotOp(AST):
    def __init__(
            self, value: Union['BinOp', Value],
            operation: TOKEN
    ):
        self.value = value
        self.operation = operation
