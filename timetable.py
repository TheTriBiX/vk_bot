import requests
import datetime


def create_timetable(name, today_date):
    table = ''
    id_request = requests.get(f'https://ruz.hse.ru/api/search?term={name}&type=student')
    user_id = id_request.json()[0]['id']
    r = requests.get(f'https://ruz.hse.ru/api/schedule/student/{user_id}?start={today_date}&finish={today_date}&lng=1')
    if r.json():
        for i in r.json():
            table += f'''{i['discipline']}({i['kindOfWork']}) 
            {i['beginLesson']} - {i['endLesson']}
            Ссылка на занятие - {i['url1']}\n'''
        return 'Расписание на сегодня:\n' + table
    else:
        return None
