import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3

with open('token.txt') as f:
    API_TOKEN = str(f.readline())
vk = vk_api.VkApi(token=API_TOKEN)
conn = sqlite3.connect('users.db')
cur = conn.cursor()


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
    for event in VkLongPoll(vk).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            if msg == "начать":
                send_message(user_id, 'Начинаем регистрацию!')
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Староста', VkKeyboardColor.PRIMARY)
                keyboard.add_button('Ученик', VkKeyboardColor.NEGATIVE)
                send_message(user_id, "тыкни кнопку", keyboard)

            if msg in ['староста', 'ученик']:
                role = msg
                cur.execute(f"""SELECT id FROM user_role WHERE id={user_id}""")
                if cur.fetchone():
                    send_message(user_id, 'Ты уже зарегистрирован.')
                else:
                    cur.execute("""INSERT INTO user_role(id, role)
                                 VALUES(?, ?);""", (user_id, role))
                    send_message(user_id, f'Поздравляю, можешь продолжать.')
                    conn.commit()
