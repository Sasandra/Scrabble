"""Implementation for Computer AI"""

import pickle
import os
from Back.Tree import Tree
from Back.Tree import Node

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
TREE_PATH = os.path.join(THIS_DIR, "pickledtree.txt")


class ComputerAI:
    """ Computer PLAYER """

    def __init__(self, player, letter_set):
        self.player = player
        self.letter_set = letter_set
        self.tree = pickle.load(open(TREE_PATH, 'rb'))
        self.possible_words = list()

    def find_possible_words(self, letter):
        """
        :param letter: letter from BOARD
        :return: list of all possible WORDS created from holder and letter from BOARD
        """
        temp_holder = list()
        temp_holder.extend(self.player.holder)
        temp_holder.extend(letter)
        found = dict()

        if letter in found:
            return found[letter]
        else:
            found[letter] = self.tree.find_all_words(temp_holder)
            return found[letter]

    def remove_incorrect_words(self, letter):
        """
        :param letter: letter from BOARD
        :return: updated list if any letter doesn't contain letter
        """
        cleaned_list = list()

        for word in self.possible_words:
            if letter in word:
                cleaned_list.append(word)

        return cleaned_list

    @staticmethod
    def split_word(letter, word):
        """
        :param letter: letter which split word
        :param word: word to split
        :return: pair of splited word, without given letter (to put on BOARD)
        """
        temp = list(word)
        index = temp.index(letter)

        return ''.join(temp[:index]), ''.join(temp[index + 1:])

    def split_list(self, letter):
        """
        :param letter: letter to split on it
        :return: list of WORDS splited on given letter
        """

        self.possible_words = self.remove_incorrect_words(letter)
        splited_list = list()

        for word in self.possible_words:
            splited_list.append(self.split_word(letter, word))

        return splited_list

    @staticmethod
    def check_list(letter, splited_words, space_from_edge):
        """
        :param letter: letter which splited word
        :param splited_words: list of WORDS splited by given letter
        :param space_from_edge: distance to BOARD edge (or other tiles)
        :return: list of WORDS which are in BOARD range
        """
        correct_words = []
        for element in splited_words:
            if len(element[0]) <= space_from_edge[0] and len(element[1]) <= space_from_edge[1]:
                correct_words.append((element[0], letter, element[1]))
        return correct_words

    def get_word_score(self, splited_word):
        """
        :param splited_word: splited word
        :return: score for this word, without premiums
        """
        score = 0
        word = ''
        for part in splited_word:
            word += part

        for i in word:
            score += self.letter_set.get_points(i)

        return score

    def get_max_score(self, splited_words):
        """
        :param splited_words: list of splited WORDS
        :return: tuple, word and score when score is max
        """
        scores = list()
        for word in splited_words:
            score = self.get_word_score(word)
            scores.append((score, word))

        if scores:
            return max(scores)
        else:
            return False

    def find_best_word(self, letter, space_from_edge):
        """
        :param letter: read from BOARD
        :param space_from_edge: distance to BOARD'edges (or other tiles)
        :return: tuple: word and score for it or false if word wasn't found
        """
        self.possible_words = self.find_possible_words(letter)
        splited_words_list = self.split_list(letter)
        correct_words_list = self.check_list(letter, splited_words_list, space_from_edge)

        if correct_words_list:
            return self.get_max_score(correct_words_list)
        else:
            return False

    def find_move(self, collisions):
        """
        :param collisions: list of collisions :[MovingLetter, row_space, column_space]
        :return: best scored word, or fale if such word doesn't exist
        """
        possible_words = list()
        for col in collisions:
            if col[1] != [0, 0]:
                if self.find_best_word(col[0].letter, col[1]):
                    possible_words.append([self.find_best_word(col[0].letter, col[1]), 'r', col[0].position])

            elif col[2] != [0, 0]:
                if self.find_best_word(col[0].letter, col[2]):
                    possible_words.append([self.find_best_word(col[0].letter, col[2]), 'c', col[0].position])

        if not all(item is False for item in possible_words):
            return max(possible_words)
        else:
            return False
