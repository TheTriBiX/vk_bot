import unittest
from easteregg_functions import visit_para
from timetable import create_timetable
from Deadline import deadline
from main import send_message
import vk_api


class TestVisitPara(unittest.TestCase):

    def test_the_only_two_possible(self):
        self.assertEqual(visit_para(), 'Иди!' or 'Фиг с ней, не иди')

    def test_classtable_work(self):
        self.assertEqual((create_timetable('Семенищев Матвей Владимирович', '2021.12.18')).replace('\n', ''), """Расписание на сегодня:
Алгоритмизация и программирование (рус)(Семинар Online) 
            09:30 - 10:50
            Ссылка на занятие - https://discord.gg/xF5PYvb8
Алгоритмизация и программирование (рус)(Практическое занятие) 
            11:10 - 12:30
            Ссылка на занятие - None
История (рус)(Семинар Online) 
            14:40 - 16:00
            Ссылка на занятие - https://univ-eiffel.zoom.us/j/83975625022


""".replace('\n', ''))

    def test_classtable_wrong_name(self):
        with self.assertRaises(IndexError):
            create_timetable('фывоарлфыв', '2021.12.17')

    def test_classtable_wrong_date(self):
        self.assertEqual(create_timetable('Семенищев Матвей Владимирович', 'фывфы'), None)

    def test_deadline_type(self):
        self.assertEqual(deadline('аип').fetchone()[1], 'Проект')

    def test_deadline_subject(self):
        self.assertEqual(deadline('асис').fetchone()[0], 'асис')

    def test_unknown_keyboard(self):
        with self.assertRaises(AttributeError):
            send_message(1, 'asd', 'asd')

    def test_unknown_message(self):
        with self.assertRaises(vk_api.exceptions.ApiError):
            send_message(1, 456)

    def test_message(self):
        with self.assertRaises(vk_api.exceptions.ApiError):
            send_message('boba', 'biba')


if __name__ == '__main__':
    unittest.main()
