import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3
from Deadline import deadline, edit_deadline
from timetable import create_timetable
from Questions import ask_questions, checktell_answer, answer_question
from announcement import create_announcement
from easteregg_functions import visit_para, grade_bar, show_bars

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
    if cur.execute(f"""SELECT role FROM user_role WHERE id={user_id}""").fetchone()[0] == 'староста':
        keyboard.add_button('Редактирование информации', VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Приколюшки')
    send_message(user_id, "Что ты хочешь узнать?", keyboard)


def create_starostamenu(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Добавить дедлайны')
    keyboard.add_button('Ответить на вопрос')
    keyboard.add_button('Сделать объявление')
    keyboard.add_button('Помощь', VkKeyboardColor.PRIMARY)
    send_message(user_id, "Выбери пункт", keyboard)


def create_funmenu(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Идти ли на пару?')
    keyboard.add_button('Оценить бары Москвы')
    keyboard.add_button('Посмотреть оценки баров Москвы')
    keyboard.add_button('Помощь', VkKeyboardColor.PRIMARY)
    send_message(user_id, "Выбирай!", keyboard)


if __name__ == '__main__':
    print('starting...')
    quest = 0
    dead = 0
    question = None
    announce = 0
    bars = 0
    stage = 0
    lis = []
    lis_bar = []
    for event in VkLongPoll(vk).listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            user_id = event.user_id

            if msg == 'редактирование информации':
                if cur.execute(f"""SELECT role FROM user_role WHERE id={user_id}""").fetchone()[0] == 'староста':
                    create_starostamenu(user_id)
                else:
                    send_message(user_id, 'Кто-то попытался сломать систему, но система сильнее BibleThump')

            if quest == 1:
                ask_questions(user_id, msg)
                send_message(user_id, "мы уведомили старосту, жди ответа")
                quest = 0
                create_mainmenu(user_id)

            if question:
                answer_question(question, msg)
                question = None
                create_mainmenu(user_id)

            if msg == 'ответить на вопрос':
                question = checktell_answer()

            if msg == 'приколюшки':
                create_funmenu(user_id)

            if announce == 1:
                announce = 0
                create_announcement(msg)

            if msg == 'идти ли на пару?':
                answer = visit_para()
                send_message(user_id, answer)
                create_funmenu(user_id)

            if msg == 'оценить бары москвы':
                bars = 1
                send_message(user_id, 'Какой бар? Напиши название.')
            elif bars == 1:
                lis_bar.append(msg)
                send_message(user_id, 'Название добавлено')
                bars = 2
                send_message(user_id, 'Как бы ты оценил бар?')
            elif bars == 2:
                lis_bar.append(msg)
                send_message(user_id, 'Оценка добавлена')
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Добавить описание бара')
                keyboard.add_button('Не добавлять описание бара')
                send_message(user_id, 'Добавить описание бара?', keyboard)
                bars = 3
            elif msg == 'добавить описание бара':
                bars = 4
                send_message(user_id, 'Какое описание бара?')
            elif bars == 4:
                lis_bar.append(msg)
                grade_bar(bars, lis_bar)
                bars = 0
                lis_bar = []
                send_message(user_id, 'Оценка бара добавлен')
                create_mainmenu(user_id)
            elif msg == 'не добавлять описание бара':
                bars = 3
                grade_bar(bars, lis_bar)
                send_message(user_id, 'Оценка бара добавлена')
                bars = 0
                lis_bar = []
                create_mainmenu(user_id)

            if msg == 'посмотреть оценки баров москвы':
                all_info = show_bars()
                for bar in all_info:
                    message = ''
                    for data in bar:
                        if data != None:
                            message += str(data)
                            message += ' - '
                    message = message[:-3]
                    send_message(user_id, message)
                create_mainmenu(user_id)

            if msg == 'сделать объявление':
                announce = 1
                send_message(184299452, 'Что должны узнать все студенты в группе?')

            if msg == "начать":
                if cur.execute(f"""SELECT id FROM user_role WHERE id={user_id}""").fetchone():
                    send_message(user_id, 'Вы уже зарегистрированы, длы вызова меню напишите "помощь"')
                else:
                    send_message(user_id, 'Начинаем регистрацию!')
                    keyboard = VkKeyboard(one_time=True)
                    keyboard.add_button('Староста', VkKeyboardColor.PRIMARY)
                    keyboard.add_button('Ученик', VkKeyboardColor.NEGATIVE)
                    send_message(user_id, 'Выбери кнопку', keyboard)

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
                keyboard.add_button('Все дедлайны', VkKeyboardColor.PRIMARY)
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

            if msg == 'добавить дедлайны':
                stage = 1
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('АиП')
                keyboard.add_button('АСиС')
                keyboard.add_button('Инфа')
                keyboard.add_button('Матан')
                send_message(user_id, 'Какой предмет? Нажми кнопку или напиши предмет.', keyboard)
            elif stage == 1:
                lis.append(msg)
                send_message(user_id, 'Предмет добавлен')
                stage = 2
                send_message(user_id, 'Какой тип работы?')
            elif stage == 2:
                lis.append(msg)
                send_message(user_id, 'Тип работы добавлен')
                stage = 3
                send_message(user_id, 'Какая дата?')
            elif stage == 3:
                lis.append(msg)
                send_message(user_id, 'Дата добавлена')
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Добавить описание')
                keyboard.add_button('Не добавлять описание')
                send_message(user_id, 'Добавить описание?', keyboard)
                stage = 4
            elif msg == 'добавить описание':
                stage = 5
                send_message(user_id, 'Какое описание?')
            elif stage == 5:
                lis.append(msg)
                edit_deadline(stage, lis)
                stage = 0
                lis = []
                send_message(user_id, 'Дедлайн добавлен')
                create_mainmenu(user_id)
            elif msg == 'не добавлять описание':
                stage = 4
                edit_deadline(stage, lis)
                send_message(user_id, 'Дедлайн добавлен')
                stage = 0
                lis = []
                create_mainmenu(user_id)
