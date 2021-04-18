"""Module with DNF analyzer"""

from typing import Union, Optional

from modules.lexer.lexer import Lexer
from modules.parser.parser import Parser
from modules.parser.ast_nodes import BinOp, NotOp, Value
from modules.utils import (
    NotSimpleConjunctionBadOperation,
    BadTokensForDNF,
    NotSimpleConjunctionBadNot,
    NotSimpleConjunctionSameValues
)
from modules.tokens import (
    EOF, CONST, SYBMOL,
    OPEN_BRACKET, CLOSE_BRACKET,
    AND_OPERATOR, OR_OPERATOR,
    NOT_OPERATOR, IMPLICATION,
    EQUIVALENCE, TOKEN
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

    @staticmethod
    def __check_values(node):
        if isinstance(node, BinOp):
            if isinstance(node.left, Value) and isinstance(node.right, Value):
                if node.left.value == node.right.value:
                    raise NotSimpleConjunctionSameValues(
                        f'Same values for node: {node}\n'
                        f'Left: {node.left.value} | '
                        f'Right: {node.right.value}'
                    )
            if isinstance(node.left, NotOp) and isinstance(node.right, Value):
                if isinstance(node.left.value, Value):
                    if node.left.value.value == node.right.value:
                        raise NotSimpleConjunctionSameValues(
                            f'Same values for node: {node}\n'
                            f'Left: !{node.left.value.value} | '
                            f'Right: {node.right.value}'
                        )
            if isinstance(node.left, Value) and isinstance(node.right, NotOp):
                if isinstance(node.right.value, Value):
                    if node.left.value == node.right.value.value:
                        raise NotSimpleConjunctionSameValues(
                            f'Same values for node: {node}\n'
                            f'Left: {node.left.value} | '
                            f'Right: !{node.right.value.value}'
                        )

    def __analyzing(
            self, root: Union[NotOp, BinOp],
    ):
        self.__check_tokens(node=root)
        self.__check_values(node=root)

        is_dnf = True

        if isinstance(root, BinOp):
            self.__check_values(node=root.left)
            self.__check_values(node=root.right)

            if isinstance(root.left, Value) and isinstance(root.right, Value):
                if isinstance(root.operation, AND_OPERATOR):
                    return True
                else:
                    raise NotSimpleConjunctionBadOperation(
                        f'{root} is not simple conjunction. '
                        f'Op: {root.operation} Left: {root.left} Right: {root.right}'
                    )

            if not isinstance(root.left, Value):
                is_dnf = self.__analyzing(root.left)

                if is_dnf:
                    if isinstance(root.operation, AND_OPERATOR):
                        is_dnf = True
                    elif not isinstance(root.operation, OR_OPERATOR) and \
                            not isinstance(root.left, NotOp):
                        return False
                    elif isinstance(root.operation, OR_OPERATOR) and isinstance(root.left, NotOp):
                        return False
                else:
                    return False

            if not isinstance(root.right, Value):
                is_dnf = self.__analyzing(root.right)

                if is_dnf:
                    if isinstance(root.operation, AND_OPERATOR):
                        is_dnf = True
                    elif not isinstance(root.operation, OR_OPERATOR) and \
                            not isinstance(root.right, NotOp):
                        return False
                    elif isinstance(root.operation, OR_OPERATOR) and isinstance(root.right, NotOp):
                        return False
                else:
                    return False

        elif isinstance(root, NotOp):
            self.__check_values(node=root.value)

            if isinstance(root.value, Value):
                return True
            else:
                raise NotSimpleConjunctionBadNot(
                    f'{root} is not simple conjunction. '
                    f'Op: {root.operation} Value: {root.value}'
                )

        return is_dnf
