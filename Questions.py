import sqlite3
conn = sqlite3.connect('users.db')
cur = conn.cursor()


def ask_questions(user_id, msg):
        cur.execute("""INSERT INTO questions(id, question)
                                 VALUES(?, ?);""", (user_id, msg))
