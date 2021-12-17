import random
import sqlite3 as sq


def visit_para():
    """Функция visit_para() не принимает на вход никаких аргументов, отдает на выход
    одну из двух возможных строк, итоговая строка выбирается рандомно."""
    possible = ['Иди!', 'Фиг с ней, не иди']
    answer = random.choice(possible)
    return answer


def grade_bar(stage, msg):
    """
    Функция, которая служит для добавления оценки бара студентом в БД
    :param stage: int, определяет вариант, который запишется в базу данных - с описанием или без
    :param msg: список, состоящий либо из 2-х, либо из 3-х элементов: название бара, оценка студента и описание
    """
    with sq.connect("users.db") as db:
        cur = db.cursor()
        if stage == 3:
            cur.execute("""INSERT INTO bars (name, grade) VALUES (?, ?)""",
                        (msg))
        elif stage == 4:
            cur.execute("""INSERT INTO bars (name, grade, description) VALUES (?, ?, ?)""",
                        (msg))


def show_bars():
    """
    Функция, которая показывает оценки баров студентами
    :return: возвращает объект курсора базы данных, который содержит всю информацию из БД
    """
    with sq.connect("users.db") as db:
        cur = db.cursor()
    a = """SELECT * FROM bars"""
    cur.execute(a)
    return cur
