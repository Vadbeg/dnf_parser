"""Module with tests"""

from typing import List

from modules.semantic_analyzer.dnf_analyzer import DNFAnalyzer

TEST_CASES = [
    (r'((((((!A)/\B)/\(!C))\/(A/\((!B)/\(!C))))\/((B/\(!A))/\(!C))))', True),
    (r'(((A/\A)\/(A/\(!B))))', Exception)
    r'(((A/\B)\/(A/\(!B))))',
    r'(((A/\B)\/(A/\(!B)))A)',
    r'(((A/\B)\/(A/\(!B))))',
    r'(((A/\B)\/(A/\(!(!B)))))',
    r'(((A/\(!B))\/(A/\(!B))))',
    r'((((!A)/\B)\/(A/\(!B))))',
    r'((((!A)/\B)\/(A/\(!B))))',
    r'((((!A)/\B)\/(A/\(!B))))',
    r'((((((!A)/\B)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C))))',
    r'((((((!A)\/B)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C))))',
    r'((((((!A)/\B)/\((!C)/\A))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C))))',
    r'((((((!A)/\D)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C))))',
    '',
    ' ',
    '1',
    '0',
    r'(A/\B)',
    r'(A/\(!B))',
    r'(A/\(!A))',
]


def try_tests(tests: List[str]):
    for curr_test in tests:
        print(curr_test)

        try:
            dnf_analyzer = DNFAnalyzer(formula_to_analyze=curr_test)
            res = dnf_analyzer.analyze_formula()
            print(res)
        except Exception as err:
            print(err)

        print('-' * 15)


if __name__ == '__main__':
    try_tests(tests=TEST_CASES)