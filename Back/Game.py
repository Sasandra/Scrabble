""" Module for generall game functions"""
from collections import namedtuple

from numpy.core.getlimits import iinfo

from Back import WordsList

MovingLetter = namedtuple('MovingLetter', 'letter, position')


class Game:
    def __init__(self, words_list=None, players=None, board=None, letters=None):
        self.players = players
        self.moves_counter = 0
        self.word = list()  # list for MovingLetters
        self.words_list = words_list
        self.moving_letter = MovingLetter('', ())  # letter and its position
        self.board = board
        self.letter_set = letters
        self.current_playing_user  # user which is actually playing

    @staticmethod
    def tuple_diff(tuple1, tuple2):
        """ Calculate difference between two tuples' elements"""
        return [abs(i - j) for i, j in zip(tuple1, tuple2)]

    @staticmethod
    def is_verticall(tuples):
        """ check if letters was placed vertically"""
        print('v')
        for i in tuples:
            if i[0] != 0:
                return False
        return True

    @staticmethod
    def is_horizontal(tuples):
        """check if letters was placed horizontally """
        print('h')
        for i in tuples:
            if i[1] != 0:
                return False
        return True

    def positions_validation(self):
        """ check if letters are on one line vertically or horizontally"""
        positions_diff = list()
        for i in range(len(self.word) - 1):
            positions_diff.append(self.tuple_diff(self.word[i].position, self.word[i + 1].position))

        if self.is_horizontal(positions_diff) or self.is_verticall(positions_diff):
            return True
        else:
            return False

    def validation(self):
        """ chceck if placed letters create allowed word and if letters are in one line"""
        word = ''
        for letter in self.word:
            word += letter.letter

        if not self.words_list.find_if_word_in_list(word):
            return False

        return self.positions_validation()

    def collision_validation(self):
        """ chceck if new word create some collision"""
        pass

    def chcek_positions_availability(self):
        """chec if choseen position if empty"""
        for i in self.word:
            if self.board[i.position] != None:
                return False
        return True

    def put_word_on_board(self):
        """ mark on board letter, remove used letters form set"""
        for i in self.word:
            self.board.set_letter_on_position(i.position, i.letter)
            self.letter_set.dekrement_amount(i.letter)

    def calculate_score(self):
        """calculate score for created word"""
        score = 0
        word_factor = 1
        for i in self.word:
            if i.position in self.board.premium:
                premium = self.board.premium.get_premium_from_position(i.position)
                if premium[0] == 'word':
                    word_factor *= premium[1]
                elif premium[0] == 'letter':
                    score += self.letter_set.get_point(i.letter) * premium[1]
            else:
                score += self.letter_set.get_point(i.letter)

        score *= word_factor

        return score
