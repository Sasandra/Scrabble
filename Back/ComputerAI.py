"""Implementation for Computer AI"""

from itertools import combinations, chain
from Back import WordsList
import time


class ComputerAI:

    def __init__(self, board=None, computer_player=None, letters=None, words=None):
        self.board = board
        self.computer_player = computer_player
        self.letters = letters
        self.words = words
        self.avalible_words = dict()

    def findsubsets(self, S, m):
        return set(combinations(S, m))

    def find_possible_words_to_put(self):
        """ Find all possible words wich can be created from letters on holder"""
        t = time.time()
        words = list('konsfde')
        result = list()
        for i in range(2, len(words)+1):
            temp = self.findsubsets(words, i)
            for j in temp:
                print(j)
                result.append(self.words.find_word_match_to_letters(j))
        print(time.time() - t)

b = WordsList.Words()
a = ComputerAI(words=b)
a.find_possible_words_to_put()