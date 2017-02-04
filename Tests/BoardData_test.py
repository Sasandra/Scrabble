""" Testing BoardData module"""
import unittest
import collections
from Back import BoardData

Premium = collections.namedtuple('premium', 'kind factor')


class BoardDataTest(unittest.TestCase):
    def setUp(self):
        self.board = BoardData.Board()
        self.board.set_letter_on_position((7, 7), 'a')
        self.premium = Premium(kind='word', factor=3)

    def test_get_letter_from_position(self):
        letter = self.board.get_letter_from_position((7, 7))
        self.assertEqual(letter, 'a')

    def test_get_premium_from_position(self):
        premium = self.board.get_premium_from_position((0, 0))
        self.assertEqual(premium, self.premium)

    def test_set_letter_on_position(self):
        self.board.set_letter_on_position((7, 7), 'a')
        self.assertEqual(self.board.get_letter_from_position((7, 7)), 'a')


suite = unittest.TestLoader().loadTestsFromTestCase(BoardDataTest)
print(unittest.TextTestRunner(verbosity=3).run(suite))
