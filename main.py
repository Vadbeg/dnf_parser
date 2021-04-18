"""Entry point to project"""

from modules.lexer.lexer import Lexer
from modules.parser.parser import Parser
from modules.parser.ast_nodes import Value, BinOp, NotOp
from modules.semantic_analyzer.dnf_analyzer import DNFAnalyzer
from modules.tokens import OPEN_BRACKET, CLOSE_BRACKET


def postorder_traversal(root):
    res = list()

    if hasattr(root, 'left'):
        res.append(OPEN_BRACKET(value='('))
        res.extend(postorder_traversal(root.left))
        res.append(root)
        res.extend(postorder_traversal(root.right))
        res.append(CLOSE_BRACKET(value=')'))

    elif hasattr(root, 'value') and isinstance(root, NotOp):
        res.append(OPEN_BRACKET(value='('))
        res.append(root)
        res.extend(postorder_traversal(root.value))
        res.append(CLOSE_BRACKET(value=')'))
    else:
        res = [root]

    return res


def get_string_after_traversal(operations):
    res = ''

    for curr_operation in operations:
        if isinstance(curr_operation, Value):
            res += curr_operation.value
        elif isinstance(curr_operation, (BinOp, NotOp)):
            res += curr_operation.operation.value
        else:
            if curr_operation is not None:
                res += curr_operation.value

    return res


if __name__ == '__main__':
    formula = '((((!((!A)/\\!B)/\\(C))\\/(A/\\((B)/\\(!C))))\\/((B/\\(A))/\\(C))))'
    # formula = r'(!A)'
    # formula = r'((((((!A)/\B)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C))))'

    lexer = Lexer(string_to_parse=formula)

    lexer.parse_tokens()
    tokens = lexer.get_tokens()
    res_string = lexer.tokens_to_string(tokens=tokens)
    parser = Parser(lexer=lexer)

    node = parser.parse()

    result = postorder_traversal(node)

    res_string_again = get_string_after_traversal(operations=result)

    print(node)
    print(f'String after tree: {res_string_again}')
    # print(f'Is string after traversal equal to formula: {res_string_again == formula}')

    dnf_analyzer = DNFAnalyzer(formula_to_analyze=formula)

    res = dnf_analyzer.analyze_formula()

    print(f'Analization result: {res}')
