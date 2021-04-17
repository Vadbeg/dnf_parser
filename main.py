"""Entry point to project"""

from modules.lexer.lexer import Lexer
from modules.parser.parser import Parser


def postorder_traversal(root):
    res = list()

    if hasattr(root, 'left'):
        res.extend(postorder_traversal(root.left))
        res.append(root)
        res.extend(postorder_traversal(root.right))
    else:
        res = [root]

    return res

if __name__ == '__main__':
    # formula = '((((((!A)/\\B)/\\(!C))\\/(A/\\((!B)/\\(!C))))\\/((B/\\(!A))/\\(!C))))'
    formula = r'(A/\(B\/A))'

    lexer = Lexer(string_to_parse=formula)

    lexer.parse_tokens()
    tokens = lexer.get_tokens()
    res_string = lexer.tokens_to_string(tokens=tokens)

    print(f'Tokens out of lexer: {tokens}')
    print(f'String from tokens: {res_string}')
    print(f'Is string from tokens equal to formula: {res_string == formula}')

    parser = Parser(lexer=lexer)

    node = parser.parse()

    result = postorder_traversal(node)

    res_string_again = Lexer.tokens_to_string(tokens=tokens)

    print(f'String after tree: {res_string_again}')
    print(f'Is string after traversal equal to formula: {res_string_again == formula}')
