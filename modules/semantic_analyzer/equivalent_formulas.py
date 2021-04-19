"""
Лабораторная работа №2 по дисциплине ЛОИС
Вариант F: Проверить, является ли формула ДНФ
Выполнена студентом группы 821701 БГУИР Титко Вадим Сергеевич
Файл с функциями алгоритма
"""

"""Module for checking if values are equivalent"""


import itertools
from typing import List, Dict, Union

from modules.lexer.lexer import Lexer
from modules.parser.parser import Parser
from modules.parser.ast_nodes import BinOp, NotOp, Value
from modules.interpreter.interpreter import Interpreter
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


class EquivalenceChecker:
    def __init__(self, formula_first: str, formula_second: str):
        self.__interpreter_first = Interpreter(formula_to_analyze=formula_first)
        self.__interpreter_second = Interpreter(formula_to_analyze=formula_second)

        self.__all_token_values = self.__get_all_token_values(
            interpreter_first=self.__interpreter_first,
            interpreter_second=self.__interpreter_second
        )

    @staticmethod
    def __get_all_token_values(
            interpreter_first: Interpreter,
            interpreter_second: Interpreter
    ):
        first_token_values = set(interpreter_first.unique_token_values)
        second_token_values = set(interpreter_second.unique_token_values)

        all_token_values = first_token_values.union(second_token_values)

        return all_token_values

    def __create_truth_table_input(self) -> List[Dict[str, int]]:
        table_values = list(itertools.product([0, 1], repeat=len(self.__all_token_values)))
        table = list()

        for curr_table_value in table_values:
            curr_table_row = dict(zip(self.__all_token_values, curr_table_value))

            table.append(curr_table_row)

        return table

    def check_equivalence(self):
        truth_table = self.__create_truth_table_input()

        for curr_table_row in truth_table:
            self.__interpreter_first.values = curr_table_row
            self.__interpreter_second.values = curr_table_row

            result_first = self.__interpreter_first.interpret()
            result_second = self.__interpreter_second.interpret()

            if result_first != result_second:
                return False

        return True
