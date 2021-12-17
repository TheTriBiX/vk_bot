import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
from Deadline import deadline
from timetable import create_timetable
from Questions import ask_questions, checktell_answer, answer_question

with open('token.txt') as f:
    API_TOKEN = str(f.readline())
vk = vk_api.VkApi(token=API_TOKEN)
conn = sqlite3.connect('users.db')
cur = conn.cursor()
first_time = True
fio = False


def send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': int(round(time.time() * 1000))
    }
    if keyboard:
        post["keyboard"] = keyboard.get_keyboard()
    vk.method('messages.send', post)


def create_mainmenu(user_id):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Дедлайны')
    keyboard.add_button('Расписание')
    keyboard.add_button('Задать вопрос')
    if cur.execute(f"""SELECT role FROM user_role WHERE id={user_id}""").fetchone() == 'староста':
        keyboard.add_button('Редактирование информации')
    send_message(user_id, "Что ты хочешь узнать?", keyboard)


def create_starostamenu(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('добавить дедлайны')
    keyboard.add_button('изменить расписание')
    keyboard.add_button('ответить на вопрос')
    send_message(user_id, "Что ты хочешь узнать?", keyboard)


if __name__ == '__main__':
    print('starting...')
    quest = 0
    dead = 0
    question = None
    for event in VkLongPoll(vk).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            if msg == 'редактирование информации':
                if cur.execute(f"""SELECT role FROM user_role WHERE id={user_id}""").fetchone() == 'староста':
                    create_starostamenu(user_id)
                else:
                    send_message(user_id, 'Кто-то попытался сломать систему, но система сильнее BibleThump')

            if quest == 1:
                ask_questions(user_id, msg)
                send_message(user_id, "мы уведомили старосту, жди ответа")
                quest = 0
                create_mainmenu(user_id)

            if msg == 'Ответить на вопрос':
                question = checktell_answer()

            if question:
                answer_question(question, msg)
                question = None
                create_mainmenu(user_id)

            if msg == "начать":
                if cur.execute(f"""SELECT id FROM user_role WHERE id={user_id}""").fetchone():
                    send_message(user_id, 'Вы уже зарегистрированы, длы вызова меню напишите "помощь"')
                else:
                    send_message(user_id, 'Начинаем регистрацию!')
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Староста', VkKeyboardColor.PRIMARY)
                    keyboard.add_button('Ученик', VkKeyboardColor.NEGATIVE)
                    send_message(user_id, 'тыкни кнопку', keyboard)

            if msg in ['староста', 'ученик'] and not cur.execute(
                    f"""SELECT id FROM user_role WHERE id={user_id}""").fetchone():
                role = msg
                cur.execute("""INSERT INTO user_role(id, role)
                             VALUES(?, ?);""", (user_id, role))
                send_message(user_id, f'Поздравляю, можешь продолжать. Для продолжения напиши "имя"')
                conn.commit()

            if fio and msg != 'имя':
                print(msg)
                cur.execute(f"""UPDATE user_role
                                SET fullname='{str(msg)}'
                                WHERE id={user_id};""", )
                fio = False
                send_message(user_id, "Все готово! Для вызова меня напиши 'помощь'.\n"
                                      "Если ошибся в написаниии ФИО напиши: смена ФИО")
                conn.commit()

            if msg == 'имя':
                send_message(user_id, "Напиши свое ФИО\n пример: Иванов Иван Иванович")
                fio = True

            if msg == "помощь":
                create_mainmenu(user_id)

            if msg == "дедлайны":
                send_message(user_id, 'Выбор предмета')
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('АиП')
                keyboard.add_button('АСиС')
                keyboard.add_button('Инфа')
                keyboard.add_button('Матан')
                keyboard.add_button('Все дедлайны')
                send_message(user_id, 'тыкни кнопку', keyboard)
                dead = 1

            if dead == 1 and msg != "дедлайны":
                a = deadline(msg)
                dead = 0
                for i in a:
                    message = ''
                    for object in i:
                        if object != None:
                            message += str(object)
                            message += ' - '
                    message = message[:-3]
                    send_message(user_id, message)
                create_mainmenu(user_id)

            if msg == 'расписание' and cur.execute(
                    f"""SELECT fullname FROM user_role WHERE id={user_id}""").fetchone()[0]:
                send_message(user_id, create_timetable(cur.execute(
                    f"""SELECT fullname FROM user_role WHERE id={user_id}""").fetchone()[0]))

            if msg == 'задать вопрос':
                quest = 1
                send_message(user_id, 'Что ты хочешь узнать?')

            if msg == 'смена ФИО':
                fio = True
                send_message(user_id, "Напиши свое ФИО\n пример: Иванов Иван Иванович")
