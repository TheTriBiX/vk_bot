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


def checktell_answer(user_id, msg):
    question = cur.execute("""SELECT question FROM questions WHERE answer NOT IN ('ответ')""").fetchall()[0]
    if not question:
        send_message(user_id, 'вопросов больше не осталось')
        return None
    else:
        send_message(184299452, f'Вопрос, на который просят ответа: {msg}')
        return question


def answer_question(question, answer):
    user_id = cur.execute(f"SELECT id FROM question WHERE question={question}").fetchall()[0]
    send_message(user_id, f'Дорогой(ая) и любимый(ая) староста ответил(а) на твой вопрос: {answer}')