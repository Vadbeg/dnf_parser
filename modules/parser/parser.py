"""Module with parser"""

from typing import Type, Union

from modules.parser.ast_nodes import BinOp, NotOp, Value
from modules.lexer.lexer import Lexer
from modules.utils import InvalidSyntax
from modules.tokens import (
    EOF, CONST, SYBMOL,
    OPEN_BRACKET, CLOSE_BRACKET,
    AND_OPERATOR, OR_OPERATOR,
    NOT_OPERATOR, IMPLICATION,
    EQUIVALENCE, TOKEN
)


class Parser:
    def __init__(self, lexer: Lexer):
        self.__lexer = lexer

        self.__current_token = self.__lexer.peek()
        self.__token_index = 0

    def __eat(self, token_type: Type[TOKEN]):
        token = self.__current_token

        if isinstance(token, token_type):
            self.__token_index += 1
            self.__current_token = self.__lexer.peek(index=self.__token_index)
        else:
            raise InvalidSyntax(f'Invalid syntax on index: {self.__token_index} with type: {token_type}')

    def __factor(self) -> Union[BinOp, Value]:
        token = self.__current_token

        if isinstance(token, (CONST, SYBMOL)):
            self.__eat(type(token))

            return Value(token=token)
        elif isinstance(token, OPEN_BRACKET):
            self.__eat(OPEN_BRACKET)
            node = self.__expr()  # TODO: Change it!
            self.__eat(CLOSE_BRACKET)

            return node

    def __term(self) -> Union[BinOp, Value]:
        left_node = self.__factor()

        while isinstance(
                self.__current_token,
                (AND_OPERATOR, OR_OPERATOR,
                 IMPLICATION, EQUIVALENCE)
        ):
            token = self.__current_token

            self.__eat(type(token))

            right_node = self.__factor()
            left_node = BinOp(left=left_node, operation=token, right=right_node)

        return left_node

    def __expr(self):
        node = self.__term()

        print(f'Node: {node} is_in_return: {not isinstance(self.__current_token, NOT_OPERATOR)}')

        while isinstance(
                self.__current_token, NOT_OPERATOR
        ):
            token = self.__current_token

            self.__eat(type(token))

            value_node = self.__factor()
            node = NotOp(value=value_node, operation=token)

        return node

    def parse(self) -> Union[BinOp, Value]:
        return self.__expr()
