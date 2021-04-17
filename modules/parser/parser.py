"""Module with parser"""

from typing import Type, Union

from modules.parser.ast_nodes import BinOp, Value
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
        self.lexer = lexer

        self.current_token = self.lexer.peek()
        self.token_index = 0

    def eat(self, token_type: Type[TOKEN]):
        token = self.current_token

        if isinstance(token, token_type):
            self.token_index += 1
            self.current_token = self.lexer.peek(index=self.token_index)
        else:
            raise InvalidSyntax(f'Invalid syntax on index: {self.token_index}')

    def factor(self) -> Union[BinOp, Value]:
        token = self.current_token

        if isinstance(token, (CONST, SYBMOL)):
            self.eat(type(token))

            return Value(token=token)
        elif isinstance(token, OPEN_BRACKET):
            self.eat(OPEN_BRACKET)
            node = self.term()  # TODO: Change it!
            self.eat(CLOSE_BRACKET)

            return node

    def term(self):
        left_node = self.factor()

        while isinstance(
                self.current_token,
                (AND_OPERATOR, OR_OPERATOR)
        ):
            token = self.current_token

            self.eat(type(token))

            right_node = self.factor()
            left_node = BinOp(left=left_node, operation=token, right=right_node)

        return left_node

    def expr(self):
        node = self.term()

    def parse(self):
        return self.term()
