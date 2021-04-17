"""Module with lexer"""

from typing import Union

from modules.lexer.characters_reader import CharReader
from modules.tokens import (
    EOF, CONST, SYBMOL,
    OPEN_BRACKET, CLOSE_BRACKET,
    AND_OPERATOR, OR_OPERATOR,
    NOT_OPERATOR, IMPLICATION,
    EQUIVALENCE, TOKEN
)
from modules.utils import NoTokenError


class Lexer:
    def __init__(self, string_to_parse: str):
        self.char_reader = CharReader(string_to_parse=string_to_parse)

        self.__resulted_tokens = list()

    def parse_tokens(self):
        curr_char = self.char_reader.peek()
        index: int = 0

        while not isinstance(curr_char, EOF):
            curr_token = EOF()

            if CONST.is_const(curr_char):
                curr_token = CONST(curr_char)

            elif SYBMOL.is_symbol(curr_char):
                curr_token = SYBMOL(curr_char)

            elif OPEN_BRACKET.is_open_bracket(curr_char):
                curr_token = OPEN_BRACKET(curr_char)

            elif CLOSE_BRACKET.is_close_bracket(curr_char):
                curr_token = CLOSE_BRACKET(curr_char)

            elif curr_char == '/' and self.char_reader.peek(index + 1) == '\\':
                value = curr_char + self.char_reader.peek(index + 1)
                curr_token = AND_OPERATOR(value=value)

                index += 1

            elif curr_char == '\\' and self.char_reader.peek(index + 1) == '/':
                value = curr_char + self.char_reader.peek(index + 1)
                curr_token = OR_OPERATOR(value=value)

                index += 1

            elif NOT_OPERATOR.is_not_operator(curr_char):
                curr_token = NOT_OPERATOR(curr_char)

            elif curr_char == '-' and self.char_reader.peek(index + 1) == '>':
                value = curr_char + self.char_reader.peek(index + 1)
                curr_token = IMPLICATION(value=value)

                index += 1

            elif EQUIVALENCE.is_equivalence(curr_char):
                curr_token = EQUIVALENCE(curr_char)

            else:
                raise NoTokenError(f'No token with such value: {curr_char} in index {index}')

            self.__resulted_tokens.append(curr_token)

            index += 1
            curr_char = self.char_reader.peek(index)

    def get_tokens(self):
        return self.__resulted_tokens

    def tokens_to_string(self):
        resulted_string = ''

        for curr_token in self.__resulted_tokens:
            resulted_string += curr_token.value

        return resulted_string

    def peek(self, index: int = 0) -> TOKEN:
        if index >= len(self.__resulted_tokens):
            # raise EOFError(f'Index {index} is bigger or equal to string length {len(self.string_to_parse)}')
            return EOF()

        token = self.__resulted_tokens[index]

        return token

    def consume(self, index: int = 0) -> TOKEN:
        if index >= len(self.__resulted_tokens):
            return EOF()

        token = self.__resulted_tokens[index]

        self.__resulted_tokens = self.__resulted_tokens[:index] + self.__resulted_tokens[index + 1:]

        return token
