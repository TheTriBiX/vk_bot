import unittest
from easteregg_functions import visit_para
from timetable import create_timetable
from Deadline import deadline


class TestVisitPara(unittest.TestCase):

    def test_the_only_two_possible(self):
        self.assertEqual(visit_para(), 'Иди!' or 'Фиг с ней, не иди')

    def test_classtable_work(self):
        self.assertEqual(create_timetable('Семенищев Матвей Владимирович', '2021.17.18'), None)

    def test_classtable_wrong_name(self):
        with self.assertRaises(IndexError):
            create_timetable('фывоарлфыв', '2021.12.17')

    def test_classtable_wrong_date(self):
        self.assertEqual(create_timetable('Семенищев Матвей Владимирович', 'фывфы'), None)

    def test_deadline_type(self):
        self.assertEqual(deadline('аип').fetchone()[1], 'Проект')

    def test_deadline_subject(self):
        self.assertEqual(deadline('асис').fetchone()[0], 'асис')




if __name__ == '__main__':
    unittest.main()
