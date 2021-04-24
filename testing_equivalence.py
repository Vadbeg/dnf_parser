"""
Лабораторная работа №2 по дисциплине ЛОИС
Вариант F: Проверить, является ли формула ДНФ
Выполнена студентом группы 821701 БГУИР Титко Вадим Сергеевич
Файл с функциями алгоритма
"""

"""Module with tests for equivalence"""

from typing import List, Tuple, Union

from modules.semantic_analyzer.equivalent_formulas import EquivalenceChecker

TEST_CASES = [
    (r'(A\/(!B))', r'((!A)\/B)', False),
    (r'(!A)', r'((!B)/\(B\/(!A)))', False),
    (r'(!A)', r'((!A)/\(B\/(!A)))', True),
    (r'(!A)', r'(!(!(!A)))', True),
    (r'(A/\(!A))', r'(B/\(!B))', True),
    (r'(P~Q)', r'(Q~P)', True),
    (r'(P->Q)', r'((!P)\/Q)', True),
    (r'(P->Q)', r'((!P)/\(!Q))', False),
    (r'0', r'((!P)/\(!Q))', False),
    (r'((!0)\/A)', r'(1\/A)', True),
    (r'((!0)\/A)', r'(1\/A)', True),
    (r'((!(A->(!B)))/\(!(B->(!A))))', r'((P->Q)/\(Q->P))', False),
    (r'((!(A->(!B)))/\(!(B->(!A))))', r'(A/\B)', True),
    (r'0', r'1', False),
    (r'0', r'(!1)', True),
]


def try_tests(tests: List[Tuple[str, str, bool]]):
    for curr_test in tests:
        print(curr_test)
        formula1 = curr_test[0]
        formula2 = curr_test[1]

        true_result = curr_test[2]

        equivalence_checker = EquivalenceChecker(formula_first=formula1, formula_second=formula2)
        res = equivalence_checker.check_equivalence()
        print(f'True: {true_result}. Pred: {res}')

        assert true_result == res

        print('-' * 15)


if __name__ == '__main__':
    try_tests(tests=TEST_CASES)

