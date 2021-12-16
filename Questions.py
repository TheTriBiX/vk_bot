import sqlite3
from basic_functions import send_message
conn = sqlite3.connect('users.db')
cur = conn.cursor()


def ask_questions(user_id, msg):
        cur.execute("""INSERT INTO questions (id, question) VALUES (?, ?)""",
                    (user_id, msg, 'ответ'))
        name = cur.execute(f"SELECT fullname FROM user_role WHERE id={user_id}").fetchone()[0]
        send_message(184299452, f'От: {name}. Вопрос: {msg}')
        send_message(user_id, 'Вопрос отправлен')


def checktell_answer():
    question = cur.execute("""SELECT question FROM questions WHERE answer NOT IN ('ответ')""").fetchone()
    if not question:
        send_message(184299452, 'вопросов больше не осталось')
        return None
    else:
        send_message(184299452, f'Вопрос, на который просят ответа: {question[0]}')
        return question[0]


def answer_question(question, answer):
    user_id = cur.execute(f"SELECT id FROM questions WHERE question={question}").fetchall()
    for user in user_id:
        send_message(user[0], f'Дорогой(ая) и любимый(ая) староста ответил(а) на твой вопрос: {answer}')
    cur.execute(f'DELETE FROM questions WHERE question={question}')