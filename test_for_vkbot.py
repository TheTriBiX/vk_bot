import unittest
from easteregg_functions import visit_para
from timetable import create_timetable


class TestVisitPara(unittest.TestCase):

    def test_the_only_two_possible(self):
        self.assertEqual(visit_para(), 'Иди!' or 'Фиг с ней, не иди')

    def test_classtable_wrong_name(self):
        self.assertEqual(create_timetable('фывоарлфыв', '2021.12.17'), None)

    def test_classtable_wrong_date(self):
        self.assertEqual(create_timetable('Семенищев Матвей Владимирович', 'фывфы'), None)


if __name__ == '__main__':
    unittest.main()
