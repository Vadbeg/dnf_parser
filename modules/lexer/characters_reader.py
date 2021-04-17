"""Module with class for Character reading"""

from typing import Union

from modules.tokens import EOF


class CharReader:
    def __init__(self, string_to_parse: str):
        self.string_to_parse = string_to_parse

    def peek(self, index: int = 0) -> Union[str, EOF]:
        if index >= len(self.string_to_parse):
            # raise EOFError(f'Index {index} is bigger or equal to string length {len(self.string_to_parse)}')
            return EOF()

        char = self.string_to_parse[index]

        return char

    def consume(self, index: int = 0) -> Union[str, EOF]:
        if index >= len(self.string_to_parse):
            return EOF()

        char = self.string_to_parse[index]

        self.string_to_parse = self.string_to_parse[:index] + self.string_to_parse[index + 1:]

        return char


if __name__ == '__main__':
    char_reader = CharReader(string_to_parse='Chocolade cake')

    print(char_reader.consume(188))
    print(char_reader.string_to_parse)
