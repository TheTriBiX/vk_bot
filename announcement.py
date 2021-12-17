from basic_functions import send_message
import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()


def create_announcement(msg):
    """
    Функция, которая делает рассылку старосты на всех учеников группы.
    :param msg: содержит сообщение, которое требуется разослать
    """
    users = cur.execute(f"SELECT id FROM user_role WHERE role='ученик'").fetchall()
    for id in users:
        send_message(id, msg)
