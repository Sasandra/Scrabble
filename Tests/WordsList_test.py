""" Testing WordsList module"""
import unittest
from Back import WordsList


class WordsListTest(unittest.TestCase):
    def setUp(self):
        self.words_list = WordsList.Words()
        self.words_list.add_used_word('ula')

    def test_add_used_word(self):
        self.words_list.add_used_word('ola')
        self.assertEqual(self.words_list.used_words, ['ula', 'ola'])

    def test_find_if_word_in_used_list_ok(self):
        result = self.words_list.find_if_word_in_used_list('ula')
        self.assertEqual(result, True)

    def test_find_if_word_in_used_list_fail(self):
        result = self.words_list.find_if_word_in_used_list('krowa')
        self.assertEqual(result, False)

    def test_find_if_word_in_list_ok(self):
        result = self.words_list.find_if_word_in_list('miś')
        self.assertEqual(result[0], True)

    def test_find_if_word_in_list_fail(self):
        result = self.words_list.find_if_word_in_list('Ola')
        self.assertEqual(result[0], False)

    def test_find_if_word_in_list_empty(self):
        result = self.words_list.find_if_word_in_list('')
        self.assertEqual(result[0], False)


suite = unittest.TestLoader().loadTestsFromTestCase(WordsListTest)
print(unittest.TextTestRunner(verbosity=3).run(suite))
