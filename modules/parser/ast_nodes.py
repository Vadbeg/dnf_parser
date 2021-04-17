"""Module with nodes for ast (abstract-syntax trees)"""


from typing import Union

from modules.tokens import TOKEN, CONST, SYBMOL


class AST:
    pass


class BinOp(AST):
    def __init__(
            self, left: Union['BinOp'],
            operation: TOKEN, right: Union['BinOp']
    ):
        self.left = left
        self.operation = operation
        self.right = right


class Value(AST):
    def __init__(self, token: Union[CONST, SYBMOL]):
        self.token = token
        self.value = token.value

