""" Module for generall game functions"""
from collections import namedtuple
from itertools import cycle

MovingLetter = namedtuple('MovingLetter', 'letter, position')


class Game:
    """Class resposible for game strategy"""

    def __init__(self, words_list=None, players=None, board=None, letters=None):
        self.players = cycle(players)
        self.players_list = players
        self.moves_counter = 0
        self.word = list()  # list for MovingLetters
        self.words_list = words_list
        self.moving_letter = MovingLetter('', ())  # letter and its position
        self.board = board
        self.letter_set = letters
        self.current_playing_user = next(self.players)  # user which is actually playing

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

    def find_missing_position(self, tuple1, tuple2):
        """ return positiob between two given"""
        diff = self.tuple_diff(tuple1, tuple2)
        if diff[0] == 2:
            return (tuple1[0] + 1, tuple1[1])
        elif diff[1] == 2:
            return (tuple1[0], tuple1[1] + 1)

    def positions_validation(self):
        """ check if letters are on one line vertically or horizontally"""
        positions_diff = list()
        for i in range(len(self.word) - 1):
            positions_diff.append(self.tuple_diff(self.word[i].position, self.word[i + 1].position))

        return self.is_horizontal(positions_diff) or self.is_verticall(positions_diff)

    def complete_word(self):
        """ read letters from board which we use to create new word"""
        for i in range(len(self.word) - 1):
            diff = self.tuple_diff(self.word[i].position, self.word[i + 1].position)
            if diff[0] == 2 or diff[1] == 2:
                position = self.find_missing_position(self.word[i].position, self.word[i + 1].position)
                letter = self.board.get_letter_from_position(position)
                if letter is None:
                    continue
                else:
                    self.word.append(MovingLetter(letter, position))
                    self.word = sorted(self.word, key=lambda word: word.position)

    def chcek_if_center(self):
        """ first word must go through (7,7) position, function chcec if it is true"""
        for i in self.word:
            if i.position == (7, 7):
                return True

        return False

    def validation(self):
        """ chceck if placed letters create allowed word and if letters are in one line"""
        flag = True

        self.word = sorted(self.word, key=lambda word: word.position)

        # check first move
        if self.moves_counter == 0:  # first word must go through center
            word = ''
            for letter in self.word:
                word += letter.letter

            if not self.chcek_if_center():
                return False
            if not self.words_list.find_if_word_in_list(word):
                return False

        else:  # next moves
            if len(self.word) > 2:  #
                self.complete_word()

            print(self.word)

            word = ''
            for letter in self.word:
                word += letter.letter

            if not self.words_list.find_if_word_in_list(word):  # word not in dictionary but it can be eg. prze-jadę
                flag = False

            if len(self.word) > 2:
                if not self.positions_validation():
                    return False

            collisions = self.collision_validation()
            if len(collisions) == 0:  # only first word can be without collisions
                return False

            if False in collisions:  # if some collision does not create a allowed word
                return False

        return flag

    @staticmethod
    def check_range(position):
        """ check if position isn't out of board"""
        x_coor = position[0]
        y_coor = position[1]

        return (0 <= x_coor < 15) and (0 <= y_coor < 15)

    def find_word_to_collision(self, position, from_where):
        """ check if collision create avalible word"""
        diff = tuple(self.tuple_diff(position, from_where.position))
        next_letter = self.board.get_letter_from_position(position)
        word = from_where.letter
        if diff[0] == 1:  # rows
            while next_letter != None:
                word += next_letter
                position = (position[0] + 1, position[1])
                next_letter = self.board.get_letter_from_position(position)
        elif diff[1] == 1:  # columns
            while next_letter != None:
                word += next_letter
                position = (position[0], position[1] + 1)
                next_letter = self.board.get_letter_from_position(position)

        return self.words_list.find_if_word_in_used_list(word)

    def collision_validation(self):
        """ chceck if new word create some collision"""
        positions = [k.position for k in self.word]
        collisions = []
        for i in self.word:
            top = (i.position[0] - 1, i.position[1])
            down = (i.position[0] + 1, i.position[1])
            left = (i.position[0], i.position[1] - 1)
            right = (i.position[0], i.position[1] + 1)
            neighbours = [top, down, left, right]

            for j in neighbours:
                if self.check_range(j) and self.board.get_letter_from_position(j) != None:
                    if j in positions:
                        continue
                    else:
                        print(self.find_word_to_collision(j, i))
                        collisions.append(self.find_word_to_collision(j, i))

        return collisions

    def put_word_on_board(self):
        """ mark on board letter, remove used letters form set"""
        for i in self.word:
            self.board.set_letter_on_position(i.position, i.letter)
            self.letter_set.dekrement_amount(i.letter)

    def change_player(self):
        """ chcange current player"""
        self.current_playing_user = next(self.players)

    def remove_letter_from_word(self, letter):
        """ remove letter from temporary words"""
        for i in self.word:
            if i.letter == letter:
                self.word.remove(i)
                return

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
                score += self.letter_set.get_points(i.letter)

        if self.moves_counter == 0:
            word_factor *= 2
        score *= word_factor

        return score

    def end_move(self):
        """ tu sum up one single move """
        if not self.validation():
            return False
        else:
            result = ''
            for i in self.word:
                result += i.letter

            self.put_word_on_board()

            self.current_playing_user.end_move_and_reset(self.calculate_score())
            self.current_playing_user = next(self.players)
            self.word = list()

            return True

    def pass_button_press(self):
        """ if pass button was clicked"""
        self.moves_counter += 1
        self.current_playing_user.increment_pass()
        self.current_playing_user = next(self.players)
        return not self.check_pass()  # if false game stop

    def quit_button_press(self):
        """if guit button was clicked game return name of winner in case of draw winner is player first on the list"""
        scores = [i.score for i in self.players_list]
        names = [j.name for j in self.players_list]

        winner_score = max(scores)
        winner_name = names[scores.index(winner_score)]

        return (winner_name, winner_score)

    def check_pass(self):
        """ chceck if all players passed more than twice"""
        pass_amounts = [i.amount_of_pass for i in self.players_list]
        return all(item >= 2 for item in pass_amounts)

    def check_type_of_field(self, pos):
        """ check type of filed from which we want to take tile """
        if pos in self.board.premium:
            return self.board.get_premium_from_position(pos)
        else:
            return None

    def create_file_name(self, pos):
        """ create filename to read to put on board when we want to take off tile"""
        premium = self.check_type_of_field(pos)
        address = "Images\\empty_"
        if premium is None:
            address += 'field'
        else:
            if premium.kind == 'letter':
                address += 'l'
            else:
                address += 'w'

            if premium.factor == 2:
                address += '2'
            else:
                address += '3'

        address += '.png'

        return address

    def get_letter_from_pos(self, pos):
        """ Method get letter from given position"""
        for i in self.word:
            if i.position == pos:
                return i.letter

# player = (PlayerData.Player('Ola'), PlayerData.Player('Adam'))
# bord = BoardData.Board()
# bord.set_letter_on_position((3, 1), 'k')
# #bord.set_letter_on_position((1, 1), 'r')
# #bord.set_letter_on_position((1, 2), 'o')
# #bord.set_letter_on_position((1, 3), 'b')
# #bord.set_letter_on_position((1, 4), 'a')
# #bord.set_letter_on_position((1, 5), 'k')
# #bord.set_letter_on_position((6, 2), 'b')
# #bord.set_letter_on_position((7, 2), 'a')
# #bord.set_letter_on_position((8, 2), 'l')
#
# lista = WordsList.Words()
# lista.add_used_word('robak')
# lista.add_used_word('bal')
# word = list()
# a = MovingLetter('t', (0, 1))
# # b = MovingLetter('r', (1, 1))
# c = MovingLetter('a', (2, 1))
# d = MovingLetter('t', (4, 1))
# e = MovingLetter('o', (5, 1))
# f = MovingLetter('r', (6, 1))
# word.append(a)
# # word.append(b)
# word.append(c)
# word.append(d)
# word.append(e)
# word.append(f)
# # print(sorted(word, key=lambda word: word.position))
# for i in word:
#     bord.set_letter_on_position(i.position, i.letter)
#
# g = Game(words_list=lista, board=bord, players=player)
# g.word = word
# print(g.validation())
#
# for i in range(15):
#     for j in range(15):
#         if bord.board[i, j] == None:
#             print('_', end=' ')
#         else:
#             print(bord.board[i, j], end=' ')
#     ol()
