"""Module with interpreter for parser"""

from typing import List, Dict

from modules.lexer.lexer import Lexer
from modules.parser.parser2 import Parser
from modules.parser.ast_nodes import BinOp, NotOp, Value
from modules.utils import (
    BadTokensForDNF,
)
from modules.tokens import (
    CONST, SYBMOL,
)


class Interpreter:
    def __init__(self, formula_to_analyze: str):
        self.formula_to_analyze = formula_to_analyze

        self.__values = None
        self.__unique_token_values = None

        self.__parser = self.__create_parser()

    def __create_parser(self):
        lexer = Lexer(string_to_parse=self.formula_to_analyze)
        lexer.parse_tokens()

        self.__unique_token_values = self.__get_unique_symbol_values(tokens=lexer.get_tokens())

        parser = Parser(lexer=lexer)

        return parser

    @property
    def unique_token_values(self):
        if self.__unique_token_values is None:
            raise ValueError(f'No unique symbols in formula!')

        return self.__unique_token_values

    @unique_token_values.setter
    def unique_token_values(self, symbols):
        self.__unique_token_values = symbols

    @property
    def values(self) -> Dict[str, int]:
        if self.__values is None:
            raise ValueError(f'Values are not added!')

        return self.__values

    @values.setter
    def values(self, input_values: Dict[str, int]):
        self.__values = input_values

    @staticmethod
    def __check_values(unique_token_values: List[str], input_values: Dict[str, int]):
        unique_token_values = set(unique_token_values)
        unique_input_values = set(input_values.keys())

        intersection = unique_token_values.intersection(unique_input_values)

        if len(intersection) != len(unique_token_values):
            raise ValueError(f'Bad input dictionary with symbols mapping!')

    @staticmethod
    def __get_unique_symbol_values(tokens: List):
        unique_token_values = list()

        for curr_token in tokens:
            if isinstance(curr_token, SYBMOL):
                if curr_token.value not in unique_token_values:
                    unique_token_values.append(curr_token.value)

        return unique_token_values

    def __get_tree_root(self):
        root = self.__parser.parse()

        if root is None:
            raise BadTokensForDNF(f'Bad token!')

        return root

    def __get_real_value_from_value_node(self, node: Value):
        if isinstance(node.token, SYBMOL):
            value = self.values[node.value]
        elif isinstance(node.token, CONST):
            value = node.value
        else:
            raise ValueError(f'Bad token type!')

        return value

    def __perform_interpreting(self, root):
        value = 0

        if isinstance(root, BinOp):
            if isinstance(root.left, Value):
                value_left = self.__get_real_value_from_value_node(node=root.left)
            else:
                value_left = self.__perform_interpreting(root=root.left)

            if isinstance(root.right, Value):
                value_right = self.__get_real_value_from_value_node(node=root.right)
            else:
                value_right = self.__perform_interpreting(root=root.right)

            value = root.operation.apply(a=value_left, b=value_right)

        elif isinstance(root, NotOp):
            if isinstance(root.value, Value):
                value_right = self.__get_real_value_from_value_node(node=root.value)
            else:
                value_right = self.__perform_interpreting(root=root.value)

            value = root.operation.apply(a=value_right)
        elif isinstance(root, Value):
            value = self.__get_real_value_from_value_node(node=root)

        return value

    def interpret(self):
        root = self.__get_tree_root()

        self.__check_values(
            unique_token_values=self.unique_token_values,
            input_values=self.values
        )

        value = self.__perform_interpreting(root=root)

        return value
