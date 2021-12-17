import requests
import datetime


def create_timetable(name):
    table = ''
    id_request = requests.get(f'https://ruz.hse.ru/api/search?term={name}&type=student')
    user_id = id_request.json()[0]['id']
    date = datetime.datetime.now()
    today_date = f'{date.year}.{date.month}.{date.day}'
    r = requests.get(f'https://ruz.hse.ru/api/schedule/student/{user_id}?start={today_date}&finish={today_date}&lng=1')
    for i in r.json():
        if i['date'] == today_date:
            table += f'''{i['discipline']}({i['kindOfWork']}) 
            {i['beginLesson']} - {i['endLesson']}
            Ссылка на занятие - {i['url1']}\n'''
    return 'Расписание на сегодня:\n' + table
