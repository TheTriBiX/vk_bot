import sqlite3
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from basic_functions import send_message


def registration(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    send_message(user_id, 'Начинаем регистрацию!')
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Староста', VkKeyboardColor.PRIMARY)
    keyboard.add_button('Ученик', VkKeyboardColor.NEGATIVE)
    send_message(user_id, 'Выбери кнопку', keyboard)
