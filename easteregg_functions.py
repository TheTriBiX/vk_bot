from basic_functions import send_message
import random
import sqlite3
conn = sqlite3.connect('users.db')
cur = conn.cursor()


def visit_para(user_id):
    possible = ['Иди!', 'Фиг с ней, не иди']
    answer = random.choice(possible)
    send_message(user_id, answer)


def grade_bar(stage, user_id):
    pass


def show_bars(user_id):
    pass


def anek(user_id):
    pass
