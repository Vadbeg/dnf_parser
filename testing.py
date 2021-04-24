"""Module with tests"""

from typing import List, Tuple, Union

from modules.semantic_analyzer.dnf_analyzer import DNFAnalyzer

TEST_CASES = [
    (r'(((((!A)/\B)/\(!C))\/(A/\((!B)/\(!C))))\/((B/\(!A))/\(!C)))', True),
    (r'(((A/\A)\/(A/\(!B))))', Exception),
    (r'((A/\B)\/(A/\(!B)))', True),
    (r'(((A/\B)\/(A/\(!B)))A)', Exception),
    (r'((A/\B)\/(A/\(!B)))', True),
    (r'(((A/\B)\/(A/\(!(!B)))))', Exception),
    (r'((A/\(!B))\/(A/\(!B)))', True),
    (r'(((!A)/\B)\/(A/\(!B)))', True),
    (r'(((!A)/\B)\/(A/\(!B)))', True),
    (r'(((!A)/\B)\/(A/\(!B)))', True),
    (r'((!C)\/(A/\B))', True),
    (r'((A/\B)\/(!C))', True),
    (r'(((((!A)/\B)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C)))', True),
    (r'(((((!A)\/B)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C)))', Exception),
    (r'(((((!A)/\B)/\((!C)/\A))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C)))', Exception),
    (r'(((((!A)/\D)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C)))', True),
    ('', Exception),
    (' ', Exception),
    ('1', Exception),
    ('0', Exception),
    (r'(A/\)', Exception),
    (r'(B/\)', Exception),
    ('0', Exception),
    (r'(A\/B)', True),
    (r'((A\/B)\/D)', True),
    ('A', True),
    ('(!A)', True),
    (r'(A/\B)', True),
    (r'(A/\(!B))', True),
    (r'(A/\(!A))', Exception)
]


def try_tests(tests: List[Tuple[str, Union[bool, Exception]]]):
    for idx, curr_test in enumerate(tests):
        curr_formula = curr_test[0]
        curr_result = curr_test[1]

        output = None

        try:
            dnf_analyzer = DNFAnalyzer(formula_to_analyze=curr_test[0])
            output = dnf_analyzer.analyze_formula()

            assert curr_result == output, f'Formula: {curr_formula}\nCurr res: {curr_result}\nOut: {output}'
        except Exception as err:
            if isinstance(err, AssertionError):
                raise err

            if not isinstance(err, curr_result):
                raise err

            output = err

        print(f'Idx: {idx}\n'
              f'Formula: {curr_formula}\n'
              f'True result: {curr_result}\n'
              f'Output: {output}\n')
        print('-' * 15)


if __name__ == '__main__':
    try_tests(tests=TEST_CASES)
