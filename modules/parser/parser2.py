"""
Лабораторная работа №2 по дисциплине ЛОИС
Вариант F: Проверить, является ли формула ДНФ
Выполнена студентом группы 821701 БГУИР Титко Вадим Сергеевич
Файл с функциями алгоритма
"""

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
            raise InvalidSyntax(f'Invalid syntax on index: {self.__token_index + 1}. '
                                f'Got: {type(token)}. Want: {token_type}.')

    def __binary_formula(self):
        root = self.__factor()
        token = self.__current_token

        if not isinstance(token, (OR_OPERATOR, AND_OPERATOR, IMPLICATION, EQUIVALENCE)):
            raise ValueError(f'Bad syntax on {self.__token_index + 1}. '
                             f'{token} was passed')

        root = self.__handle_binary_formula(root=root, operation_type=OR_OPERATOR)
        root = self.__handle_binary_formula(root=root, operation_type=AND_OPERATOR)
        root = self.__handle_binary_formula(root=root, operation_type=IMPLICATION)
        root = self.__handle_binary_formula(root=root, operation_type=EQUIVALENCE)

        return root

    def __unary_formula(self):
        token = self.__current_token

        self.__eat(type(token))

        value_node = self.__factor()
        node = NotOp(value=value_node, operation=token)

        return node

    def __handle_binary_formula(self, root, operation_type):
        token = self.__current_token
        left_node = root

        if isinstance(token, operation_type):
            self.__eat(type(token))

            right_node = self.__factor()

            left_node = BinOp(left=left_node, operation=token, right=right_node)

        return left_node

    def __handle_formula(self):
        # next_token = self.__lexer.peek(index=self.__token_index + 1)
        token = self.__current_token

        if isinstance(token, NOT_OPERATOR):
            root = self.__unary_formula()
        else:
            root = self.__binary_formula()

        self.__eat(CLOSE_BRACKET)

        return root

    def __factor(self):
        token = self.__current_token

        if isinstance(token, OPEN_BRACKET):
            self.__eat(OPEN_BRACKET)

            root = self.__handle_formula()
        elif isinstance(token, (CONST, SYBMOL)):
            self.__eat(type(token))

            root = Value(token=token)
        else:
            raise ValueError(f'Unexpected token type for {self.__token_index}. '
                             f'You passed: {type(token)}')

        return root

    def parse(self):
        root = self.__factor()

        if self.__token_index < len(self.__lexer.get_tokens()):
            raise InvalidSyntax(f'Bad syntax!')

        return root



