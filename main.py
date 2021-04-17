"""Entry point to project"""

from modules.lexer.lexer import Lexer

if __name__ == '__main__':
    # formula = '((((((!A)/\\B)/\\(!C))\\/(A/\\((!B)/\\(!C))))\\/((B/\\(!A))/\\(!C))))'
    formula = r''

    lexer = Lexer(string_to_parse=formula)

    lexer.parse_tokens()
    tokens = lexer.get_tokens()

    print(tokens)

    res_string = lexer.tokens_to_string()

    print(res_string)

    print(res_string == formula)
    # print('\\' == '\\')
