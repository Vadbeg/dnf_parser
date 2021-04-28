"""
Лабораторная работа №2 по дисциплине ЛОИС
Вариант F: Проверить, является ли формула ДНФ
Выполнена студентом группы 821701 БГУИР Титко Вадим Сергеевич
Файл с функциями алгоритма
"""

"""Module with DNF analyzer"""

from typing import Union, Optional

from modules.lexer.lexer import Lexer
from modules.parser.parser2 import Parser
from modules.parser.ast_nodes import BinOp, NotOp, Value
from modules.utils import (
    NotSimpleConjunctionBadOperation,
    BadTokensForDNF,
    NotSimpleConjunctionSameValues,
)
from modules.tokens import (
    SYBMOL,
    AND_OPERATOR, OR_OPERATOR,
    NOT_OPERATOR
)


class DNFAnalyzer:
    GOOD_TOKENS = [
        AND_OPERATOR, OR_OPERATOR, NOT_OPERATOR, SYBMOL
    ]

    def __init__(self, formula_to_analyze: str):
        self.formula_to_analyze = formula_to_analyze

        self.__parser = self.__create_parser()

    def __create_parser(self):
        lexer = Lexer(string_to_parse=self.formula_to_analyze)
        lexer.parse_tokens()

        tokens = lexer.get_tokens()

        parser = Parser(lexer=lexer)

        return parser

    def __get_tree_root(self):
        root = self.__parser.parse()

        if root is None:
            raise BadTokensForDNF(f'Bad token!')

        return root

    def analyze_formula(self):
        root = self.__get_tree_root()

        is_dnf = self.__analyzing(root=root)

        return is_dnf

    def __check_tokens(self, node: Union[NotOp, BinOp]):

        if isinstance(node, NotOp):
            if type(node.operation) not in self.GOOD_TOKENS:
                raise BadTokensForDNF(f'Bad token: {node.operation}')

            if isinstance(node.value, Value) and \
                    type(node.value.token) not in self.GOOD_TOKENS:
                raise BadTokensForDNF(f'Bad token: {node.value.token}')

        elif isinstance(node, BinOp):
            if type(node.operation) not in self.GOOD_TOKENS:
                raise BadTokensForDNF(f'Bad token: {node.operation}')

            if isinstance(node.left, Value) and \
                    type(node.left.token) not in self.GOOD_TOKENS:
                raise BadTokensForDNF(f'Bad token: {node.left.token}')

            if isinstance(node.right, Value) and \
                    type(node.right.token) not in self.GOOD_TOKENS:
                raise BadTokensForDNF(f'Bad token: {node.right.token}')

        elif isinstance(node, Value):
            if type(node.token) not in self.GOOD_TOKENS:
                raise BadTokensForDNF(f'Bad token: {node.token}')

    def __check_values_rec(self, node: Union[BinOp, NotOp, Value]) -> list:
        node_values = list()

        if isinstance(node, BinOp) and isinstance(node.operation, AND_OPERATOR):
            node_values.extend(self.__check_values_rec(node.left))
            node_values.extend(self.__check_values_rec(node.right))

        elif isinstance(node, NotOp) and isinstance(node.value, Value):
            node_values.append(node.value.value)

        elif isinstance(node, Value):
            node_values.append(node.value)
        else:
            raise NotSimpleConjunctionBadOperation(f'Bad operation token: {node.operation}')

        return node_values

    def __check_values(self, node: Union[BinOp, NotOp, Value]):
        node_values = self.__check_values_rec(node=node)

        if len(node_values) != len(set(node_values)):
            raise NotSimpleConjunctionSameValues(f'Values: {node_values}')

    def __analyzing(
            self, root: Union[NotOp, BinOp],
    ):
        self.__check_tokens(node=root)

        is_dnf = False

        if isinstance(root, BinOp):

            if isinstance(root.operation, AND_OPERATOR):
                self.__check_values(node=root)

                return True

            if isinstance(root.operation, OR_OPERATOR):
                is_dnf_left = self.__analyzing(root=root.left)
                is_dnf_right = self.__analyzing(root=root.right)

                if is_dnf_left and is_dnf_right:
                    return True
                else:
                    return False

        elif isinstance(root, NotOp):
            self.__check_values(node=root)

            return True

        elif isinstance(root, Value):
            self.__check_values(node=root)

            return True

        return is_dnf
