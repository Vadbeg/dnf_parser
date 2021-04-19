"""
Лабораторная работа №2 по дисциплине ЛОИС
Вариант 6: Проверить, является ли формулы эквиваленты
Выполнена студентом группы 821701 БГУИР Титко Вадим Сергеевич
Файл с функциями алгоритма
"""


"""Module with testing of equivalence testing"""

from modules.semantic_analyzer.equivalent_formulas import EquivalenceChecker


if __name__ == '__main__':
    formula1 = r'(!0\/A)'
    formula2 = r'(1\/A)'

    equivalence_checker = EquivalenceChecker(formula_first=formula1, formula_second=formula2)

    res = equivalence_checker.check_equivalence()

    print(f'Are formulas equivalent: {res}')

