from basic_functions import send_message
import random
import sqlite3 as sq


def visit_para():
    possible = ['Иди!', 'Фиг с ней, не иди']
    answer = random.choice(possible)
    return answer


def grade_bar(stage, msg):
    with sq.connect("users.db") as db:
        cur = db.cursor()
        if stage == 3:
            cur.execute("""INSERT INTO bars (name, grade) VALUES (?, ?)""",
                        (msg))
        elif stage == 4:
            cur.execute("""INSERT INTO bars (name, grade, description) VALUES (?, ?, ?)""",
                        (msg))


def show_bars():
    with sq.connect("users.db") as db:
        cur = db.cursor()
    a = """SELECT * FROM bars"""
    cur.execute(a)
    return cur
