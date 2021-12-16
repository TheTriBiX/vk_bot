import time
import vk_api

with open('token.txt') as f:
    API_TOKEN = str(f.readline())
    vk = vk_api.VkApi(token=API_TOKEN)


def send_message(user_id, message, keyboard=None):
    post = {
        'user_id': user_id,
        'message': message,
        'random_id': int(round(time.time() * 1000))
    }
    if keyboard:
        post["keyboard"] = keyboard.get_keyboard()
    vk.method('messages.send', post)
