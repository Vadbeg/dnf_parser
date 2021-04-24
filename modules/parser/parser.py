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

        # self.__num_open_brackets = 0
        # self.__num_close_brackets = 0

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
            node = self.__term()  # TODO: Change it!
            self.__eat(CLOSE_BRACKET)

            return node
        elif isinstance(token, NOT_OPERATOR):
            node = self.__expr()

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

            if (left_node is None) or (right_node is None):
                raise InvalidSyntax(f'Bad values of operation: {token}')

        return left_node

    def __expr(self):
        token = self.__current_token

        self.__eat(type(token))

        value_node = self.__factor()
        node = NotOp(value=value_node, operation=token)

        return node

    def __postorder_traversal(self, root):
        res = list()

        if hasattr(root, 'left'):
            res.append(OPEN_BRACKET(value='('))
            res.extend(self.__postorder_traversal(root.left))
            res.append(root)
            res.extend(self.__postorder_traversal(root.right))
            res.append(CLOSE_BRACKET(value=')'))

        elif hasattr(root, 'value') and isinstance(root, NotOp):
            res.append(OPEN_BRACKET(value='('))
            res.append(root)
            res.extend(self.__postorder_traversal(root.value))
            res.append(CLOSE_BRACKET(value=')'))
        else:
            res = [root]

        return res

    @staticmethod
    def __get_string_after_traversal(operations):
        res = ''

        for curr_operation in operations:
            if isinstance(curr_operation, Value):
                res += str(curr_operation.value)
            elif isinstance(curr_operation, (BinOp, NotOp)):
                res += str(curr_operation.operation.value)
            else:
                if curr_operation is not None:
                    res += curr_operation.value

        return res

    def __check_brackets(self, root):
        result = self.__postorder_traversal(root)
        res_string_again = self.__get_string_after_traversal(operations=result)

        if res_string_again != self.__lexer.get_original_string():

            raise InvalidSyntax(f'Syntax is invalid. Maybe you wanted: {res_string_again}')

    def parse(self) -> Union[BinOp, Value]:
        tokens = self.__lexer.get_tokens()

        if (len(tokens) == 1) and isinstance(tokens[0], (CONST, SYBMOL)):
            pass

        elif not isinstance(self.__lexer.peek(0), OPEN_BRACKET) or \
                not isinstance(self.__lexer.peek(-1), CLOSE_BRACKET):
            raise InvalidSyntax(f'Bad main brackets!')

        parse_root = self.__term()

        self.__token_index = 0
        self.__current_token = self.__lexer.peek(0)

        self.__check_brackets(root=parse_root)

        return parse_root
