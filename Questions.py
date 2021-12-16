import sqlite3
conn = sqlite3.connect('users.db')
cur = conn.cursor()


def ask_questions(user_id, msg):
    role = cur.execute(f"""FROM user_role SELECT role WHERE id={user_id}""")
    if role == "ученик": #ask_question
        cur.execute("""INSERT INTO questions(id, question)
                                 VALUES(?, ?);""", (user_id, msg))
    else: #answer question
        pass