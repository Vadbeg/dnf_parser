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
    (r'(((((!A)\/B)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C)))', False),
    (r'(((((!A)/\B)/\((!C)/\A))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C)))', True),
    (r'(((((!A)/\D)/\(!C))\/(A/\((!B)/\(!C))))\/(((!A)/\(!B))/\(!C)))', True),
    ('', Exception),
    (' ', Exception),
    ('1', Exception),
    ('0', Exception),
    ('A', True),
    ('(!A)', True),
    (r'(A/\B)', True),
    (r'(A/\(!B))', True),
    (r'(A/\(!A))', Exception)
]


def try_tests(tests: List[Tuple[str, Union[bool, Exception]]]):
    for curr_test in tests:
        print(curr_test)
        curr_formula = curr_test[0]
        curr_result = curr_test[1]

        try:
            dnf_analyzer = DNFAnalyzer(formula_to_analyze=curr_test[0])
            res = dnf_analyzer.analyze_formula()
            print(res)

            assert curr_result == res
        except Exception as err:
            if not isinstance(err, curr_result):
                raise err

            print(err)

        print('-' * 15)


if __name__ == '__main__':
    try_tests(tests=TEST_CASES)
