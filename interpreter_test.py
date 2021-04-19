"""
Лабораторная работа №2 по дисциплине ЛОИС
Вариант F: Проверить, является ли формула ДНФ
Выполнена студентом группы 821701 БГУИР Титко Вадим Сергеевич
Файл с функциями алгоритма
"""

"""Module with interpreter testing"""

from modules.interpreter.interpreter import Interpreter


if __name__ == '__main__':
    formula = '((((!((!A)/\\!B)/\\(C))\\/(A/\\((B)/\\(!C))))\\/((B/\\(A))/\\(C))))'

    values = {
        'A': 1,
        'B': 1,
        'C': 0
    }

    interpreter = Interpreter(formula_to_analyze=formula)
    interpreter.values = values

    res = interpreter.interpret()

    print(res)
