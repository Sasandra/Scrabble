""" Testing Holder module"""
import unittest
import copy
import pygame
from Back import Holder
from Back import PlayerData
from Back import LettersSet


class HolderTest(unittest.TestCase):
    def setUp(self):
        screen = pygame.display.set_mode((1300, 670))
        player = PlayerData.Player('Ola', LettersSet.Letters())
        self.holder = Holder.Holder(player=player, screen=screen)

    def test_read_holder_letter(self):
        self.holder.read_holder()
        self.assertEqual(self.holder.holder[0][1], self.holder.player.holder[0])

    def test_read_holder_coordinates(self):
        self.holder.read_holder()
        self.assertEqual(self.holder.holder[1][0].left, 937)

    def test_change_name_polish(self):
        result = self.holder.change_name('ą')
        self.assertEqual(result, 'a1')

    def test_change_name(self):
        result = self.holder.change_name('b')
        self.assertEqual(result, 'b')

    def test_remove_from_holder(self):
        self.holder.remove_from_holder(self.holder.player.holder[-1])
        self.assertEqual(len(self.holder.holder), 6)

    def test_remove_from_holder_player(self):
        self.holder.remove_from_holder(self.holder.player.holder[-1])
        self.assertEqual(len(self.holder.holder), len(self.holder.player.holder))

    def test_return_on_holder_player(self):
        self.holder.remove_from_holder(self.holder.player.holder[-1])
        self.holder.return_on_holder('a')
        self.assertEqual(len(self.holder.holder), len(self.holder.player.holder))

    def test_return_on_holder(self):
        self.holder.remove_from_holder(self.holder.player.holder[-1])
        self.holder.remove_from_holder(self.holder.player.holder[-1])
        self.holder.return_on_holder('a')
        self.assertEqual(len(self.holder.holder), 6)

    def test_return_on_holder_test_read_holder_coordinates(self):
        self.holder.remove_from_holder(self.holder.player.holder[-1])
        self.holder.remove_from_holder(self.holder.player.holder[-1])
        self.holder.return_on_holder('a')
        self.assertEqual(self.holder.holder[5][0].left, 1165)

    def test_swap_holder(self):
        temp_holder = list()
        for i in self.holder.holder.values():
            temp_holder.append(i[1])

        a, b = temp_holder.index(self.holder.holder[0][1]), temp_holder.index(self.holder.holder[1][1])
        temp_holder[b], temp_holder[a] = temp_holder[a], temp_holder[b]

        letter_one = self.holder.holder[0][1]
        letter_two = self.holder.holder[1][1]
        self.holder.swap_letters(((0, letter_one), (1, letter_two)))
        self.assertEqual(self.holder.player.holder, temp_holder)


suite = unittest.TestLoader().loadTestsFromTestCase(HolderTest)
print(unittest.TextTestRunner(verbosity=3).run(suite))
