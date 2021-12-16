import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
from Deadline import deadline
from Questions import ask_questions

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


if __name__ == '__main__':
    print('starting...')
    quest = 0
    for event in VkLongPoll(vk).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            if quest == 1:
                ask_questions(user_id, msg)
                send_message(184299452, "мы уведомили старосту, жди ответа")
                quest = 0

            if msg == "начать":
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
                send_message(user_id, f'Поздравляю, можешь продолжать. Для продолжения напиши "помощь"')
                conn.commit()

            if fio:
                print(msg)
                cur.execute(f"""UPDATE user_role
                                SET full_name='{msg}' 
                                WHERE id={user_id};""",)

            if msg == 'имя':
                send_message(user_id, "Напиши свое ФИО\n пример: Ианов Иван Иванович")
                fio = True

            if msg == "помощь":
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Дедлайны')
                keyboard.add_button('Расписание')
                keyboard.add_button('Задать вопрос')
                send_message(user_id, "Что ты хочешь узнать?", keyboard)

            if msg == "дедлайны":
                send_message(user_id, 'Выбор предмета')
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Информатика')
                keyboard.add_button('АиП')
                keyboard.add_button('АСиС')
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

            if msg == 'расписание':
                pass

            if msg == 'задать вопрос':
                quest = 1
                send_message(user_id, 'Что ты хочешь узнать?')



