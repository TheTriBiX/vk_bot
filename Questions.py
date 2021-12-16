import sqlite3
from basic_functions import send_message
conn = sqlite3.connect('users.db')
cur = conn.cursor()


def ask_questions(user_id, msg):
        cur.execute("""INSERT INTO questions(id, question, answer)
                                 VALUES(?, ?, ?);""", (user_id, msg, None))
        name = cur.execute(f"SELECT fullname FROM user_role WHERE id={user_id}").fetchone()[0]
        send_message(184299452, f'От: {name}. Вопрос: {msg}')
        send_message(user_id, 'Вопрос отправлен')