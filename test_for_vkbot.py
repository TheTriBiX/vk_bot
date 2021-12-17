import unittest
from easteregg_functions import visit_para


class TestVisitPara(unittest.TestCase):

    def test_the_only_two_possible(self):
        self.assertEqual(visit_para(), 'Иди!' or 'Фиг с ней, не иди')


if __name__ == '__main__':
    unittest.main()