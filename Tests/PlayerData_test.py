""" Testing PlayerData module"""
import unittest
import copy
from Back import PlayerData
from Back import LettersSet


class PlayerDataTest(unittest.TestCase):
    def setUp(self):
        self.player = PlayerData.Player('Ola', LettersSet.Letters())

    def test_swap_letter(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.player.swap_letter(letters)
        self.assertEqual(self.player.holder, letters)

    def test_remove_letter_from_holder(self):
        letter_to_remove = self.player.holder[0]
        temp_holder = copy.deepcopy(self.player.holder)
        temp_holder.remove(letter_to_remove)
        self.player.remove_letter_from_holder(letter_to_remove)
        self.assertEqual(self.player.holder, temp_holder)

    def test_remove_letter_from_holder_len(self):
        letter_to_remove = self.player.holder[0]
        self.player.remove_letter_from_holder(letter_to_remove)
        self.assertEqual(len(self.player.holder), 6)

    def test_return_letter_on_holder(self):
        letter_to_remove = self.player.holder[0]
        temp_holder = copy.deepcopy(self.player.holder)
        temp_holder.remove(letter_to_remove)
        self.player.remove_letter_from_holder(letter_to_remove)
        self.player.return_letter_on_holder('b')
        temp_holder.append('b')
        self.assertEqual(self.player.holder, temp_holder)

    def test_increment_pass(self):
        self.player.increment_pass()
        self.assertEqual(self.player.amount_of_pass, 1)

    def test_update_score(self):
        self.player.update_score(20)
        self.assertEqual(self.player.score, 20)

    def test_get_name(self):
        self.assertEqual(self.player.get_name(), 'Ola')

    def test_complete_holder(self):
        self.player.remove_letter_from_holder(self.player.holder[-1])
        self.player.remove_letter_from_holder(self.player.holder[-1])
        self.player.remove_letter_from_holder(self.player.holder[-1])
        self.player.complete_holder()
        self.assertEqual(len(self.player.holder), 7)

    def test_exchange_letter(self):
        letters = list()
        letters.append(self.player.holder[-1])
        letters.append(self.player.holder[-1])
        letters.append(self.player.holder[-1])
        prev_holder = copy.deepcopy(self.player.holder)
        self.player.exchange_letter(letters)
        result = prev_holder == self.player.holder
        self.assertEqual(result, False)

    def test_end_move_and_reset_pass(self):
        self.player.end_move_and_reset(20)
        self.assertEqual(self.player.amount_of_pass, 0)

    def test_end_move_and_reset_if_change(self):
        self.player.end_move_and_reset(20)
        self.assertEqual(self.player.if_change_letters, False)

    def test_end_move_and_reset_score(self):
        self.player.end_move_and_reset(20)
        self.assertEqual(self.player.score, 20)

    def test_end_move_and_reset_holder(self):
        self.player.remove_letter_from_holder(self.player.holder[-1])
        self.player.end_move_and_reset(20)
        self.assertEqual(len(self.player.holder), 7)


suite = unittest.TestLoader().loadTestsFromTestCase(PlayerDataTest)
print(unittest.TextTestRunner(verbosity=3).run(suite))
