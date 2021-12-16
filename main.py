import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from basic_functions import send_message
from registration import registration
import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()
first_time = True


with open('token.txt') as f:
    API_TOKEN = str(f.readline())
    vk = vk_api.VkApi(token=API_TOKEN)

if __name__ == '__main__':
    print('starting...')
    for event in VkLongPoll(vk).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id
            if msg and not cur.execute(f"""SELECT id FROM user_role WHERE id={1}""").fetchone():
                registration()

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
