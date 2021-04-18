"""Module with DNF analyzer"""


from modules.lexer.lexer import Lexer
from modules.parser.parser import Parser


class DNFAnalyzer:
    def __init__(self, formula_to_analyze: str):
        self.formula_to_analyze = formula_to_analyze

        self.__parser = self.__create_parser()

    def __create_parser(self):
        lexer = Lexer(string_to_parse=self.formula_to_analyze)
        parser = Parser(lexer=lexer)

        return parser

    def __get_tree_root(self):
        root = self.__parser.parse()

        return root

    def analyze_formula(self):
        root = self.__get_tree_root()

