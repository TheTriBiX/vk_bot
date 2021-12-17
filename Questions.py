import sqlite3
from basic_functions import send_message
conn = sqlite3.connect('users.db')
cur = conn.cursor()


def ask_questions(user_id, msg):
    """
    Функция, которая уведомляет старосту о заданном вопросе, а также передает вопрос в базу данных
    :param user_id: int, содержит id пользователя, который задал вопрос
    :param msg: str, содержит вопрос, который задал пользователь
    :return:
    """
    cur.execute("""INSERT INTO questions (id, question) VALUES (?, ?)""",
                (user_id, msg))
    name = cur.execute(f"SELECT fullname FROM user_role WHERE id={user_id}").fetchone()[0]
    send_message(184299452, f'От: {name}. Вопрос: {msg}')
    send_message(user_id, 'Вопрос отправлен')
    conn.commit()


def checktell_answer():
    """
    Функция, служащая для определения наличия неотвеченных вопросов
    :return: вернет None, если вопросов больше не осталось, вернет вопрос, если вопросы еще есть.
    """
    question = cur.execute("""SELECT question FROM questions""").fetchone()
    if question == None:
        send_message(184299452, 'Вопросов больше не осталось')
        return None
    else:
        question = question[0]
        send_message(184299452, f'Вопрос, на который просят ответа: {question}')
        return question


def answer_question(question, answer):
    """
    Функция, которая служит для ответа старостой на заданный вопрос. Рассылка с ответом придет всем, кто должен получить
    ответ, если заданные ими вопросы были идентичны.
    :param question: str, содержит вопрос, который был задан
    :param answer: str, содержит ответ, который староста хочет разослать
    """
    user_id = cur.execute(f"SELECT id FROM questions WHERE question='{question}'").fetchall()
    for user in user_id:
        send_message(user[0], f'Ты задавал вопрос: {question}. '
                              f'Дорогой(ая) и любимый(ая) староста ответил(а) на твой вопрос: {answer}')
    cur.execute(f"DELETE FROM questions WHERE question='{question}'")
    conn.commit()