import sqlite3
from basic_functions import send_message
conn = sqlite3.connect('users.db')
cur = conn.cursor()


def ask_questions(user_id, msg):
        cur.execute("""INSERT INTO questions(id, question)
                                 VALUES(?, ?);""", (user_id, msg))
        send_message(184299452, f'От: {user_id}. Вопрос: {msg}')
        send_message(user_id, 'Вопрос отправлен')