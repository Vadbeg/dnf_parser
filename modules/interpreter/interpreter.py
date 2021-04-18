"""Module with interpreter for parser"""

from typing import List, Dict, Union

from modules.lexer.lexer import Lexer
from modules.parser.parser import Parser
from modules.parser.ast_nodes import BinOp, NotOp, Value
from modules.utils import (
    BadTokensForDNF,
)
from modules.tokens import (
    EOF, CONST, SYBMOL,
    OPEN_BRACKET, CLOSE_BRACKET,
    AND_OPERATOR, OR_OPERATOR,
    NOT_OPERATOR, IMPLICATION,
    EQUIVALENCE, TOKEN
)


class Interpreter:
    def __init__(self, formula_to_analyze: str):
        self.formula_to_analyze = formula_to_analyze

        self.__values = None
        self.__unique_symbols = None

        self.__parser = self.__create_parser()

    def __create_parser(self):
        lexer = Lexer(string_to_parse=self.formula_to_analyze)
        lexer.parse_tokens()

        self.__unique_symbols = self.__get_unique_symbols(tokens=lexer.get_tokens())

        parser = Parser(lexer=lexer)

        return parser

    @property
    def unique_symbols(self):
        if self.__unique_symbols is None:
            raise ValueError(f'No unique symbols in formula!')

        return self.__unique_symbols

    @unique_symbols.setter
    def unique_symbols(self, symbols):
        self.__unique_symbols = symbols

    @property
    def values(self) -> Dict[str, int]:
        if self.__values is None:
            raise ValueError(f'Values are not added!')

        return self.__values

    @values.setter
    def values(self, input_values: Dict[str, int]):
        self.__values = input_values

    @staticmethod
    def __check_values(unique_symbols: List[Value], input_values: Dict[str, int]):
        unique_token_values = set([curr_unique_symbol.value for curr_unique_symbol in unique_symbols])
        unique_input_values = set(input_values.keys())

        intersection = unique_token_values.intersection(unique_input_values)

        if len(intersection) != len(unique_token_values):
            raise ValueError(f'Bad input dictionary with symbols mapping!')

    @staticmethod
    def __get_unique_symbols(tokens: List):
        used_token_values = list()
        unique_tokens = list()

        for curr_token in tokens:
            if isinstance(curr_token, SYBMOL):
                if curr_token.value not in used_token_values:
                    used_token_values.append(curr_token.value)
                    unique_tokens.append(curr_token)

        return unique_tokens

    def __get_tree_root(self):
        root = self.__parser.parse()

        if root is None:
            raise BadTokensForDNF(f'Bad token!')

        return root

    def __perform_interpreting(self, root):
        value = 0

        if isinstance(root, BinOp):
            if isinstance(root.left, Value):
                value_left_key = root.left.value

                value_left = self.values[value_left_key]
            else:
                value_left = self.__perform_interpreting(root=root.left)

            if isinstance(root.right, Value):
                value_right_key = root.right.value

                value_right = self.values[value_right_key]
            else:
                value_right = self.__perform_interpreting(root=root.right)

            value = root.operation.apply(a=value_left, b=value_right)

        elif isinstance(root, NotOp):
            if isinstance(root.value, Value):
                value_right_key = root.value.value

                value_right = self.values[value_right_key]
            else:
                value_right = self.__perform_interpreting(root=root.value)

            value = root.operation.apply(a=value_right)

        return value

    def interpret(self):
        root = self.__get_tree_root()

        self.__check_values(
            unique_symbols=self.unique_symbols,
            input_values=self.values
        )

        value = self.__perform_interpreting(root=root)

        return value
