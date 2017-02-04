""" Testing LettersSet module"""
import unittest
from Back import LettersSet


class WordsListTest(unittest.TestCase):
    def setUp(self):
        self.letters_set = LettersSet.Letters()

    def test_get_amount(self):
        amount = LettersSet.Letters().get_amount('a')
        self.assertEqual(amount, 9)

    def test_get_points(self):
        points = self.letters_set.get_points('a')
        self.assertEqual(points, 1)

    def test_decrement_amount(self):
        amount = self.letters_set.get_amount('b')
        self.letters_set.decrement_amount('b')
        new_amount = self.letters_set.get_amount('b')
        self.assertEqual(new_amount, amount - 1)

    def test_increment_amount(self):
        amount = self.letters_set.get_amount('b')
        self.letters_set.increment_amount('b')
        new_amount = self.letters_set.get_amount('b')
        self.assertEqual(new_amount, amount + 1)

    def test_change_letters(self):
        holder = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        new_holder = self.letters_set.change_letters(holder)
        result = holder == new_holder
        self.assertEqual(result, False)

    def test_random_letters(self):
        holder = self.letters_set.random_letters(7)
        new_holder = self.letters_set.random_letters(7)
        result = holder == new_holder
        self.assertEqual(result, False)

    def test_random_letters_all(self):
        for i in range(20):
            holder = self.letters_set.random_letters(5)
        self.assertEqual(self.letters_set.number_of_letters, 0)


suite = unittest.TestLoader().loadTestsFromTestCase(WordsListTest)
print(unittest.TextTestRunner(verbosity=3).run(suite))
