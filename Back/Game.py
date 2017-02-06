""" Module for general game functions"""
from collections import namedtuple
from itertools import cycle
from Back import AIControler
from Back.Tree import Tree
from Back.Tree import Node

MovingLetter = namedtuple('MovingLetter', 'letter, position')


class Game:
    """Class responsible for GAME strategy"""

    def __init__(self, words_list, players, board, letters, ai=None):
        self.players = cycle(players)
        self.players_list = players
        self.moves_counter = 0
        self.word = list()  # list for MovingLetters
        self.words_list = words_list
        self.moving_letter = MovingLetter('', ())  # letter and its position
        self.board = board
        self.letter_set = letters
        self.current_playing_user = next(self.players)  # user which is actually playing
        self.letter_under_blank = ''
        self.allowed_word = ''
        self.created_words = list()
        self.created_word = ''

        if ai:
            self.controler_ai = AIControler.AIController(self.board, self.players_list[1], self.letter_set)

    @staticmethod
    def tuple_diff(tuple1, tuple2):
        """
        :param tuple1:
        :param tuple2:
        :return: list(!) with calculated difference between two tuples' elements
        """
        return [abs(i - j) for i, j in zip(tuple1, tuple2)]

    @staticmethod
    def is_vertically(tuples):
        """
        :param tuples: list of tuples' differences
        :return: true if word is put vertically
        """
        for i in tuples:
            if i[0] != 0:
                return False
        return True

    @staticmethod
    def is_horizontally(tuples):
        """
        :param tuples: list of tuples' differences
        :return: true if word is put horizontally
        """
        for i in tuples:
            if i[1] != 0:
                return False
        return True

    def find_missing_position(self, tuple1, tuple2):
        """
        :param tuple1: first position
        :param tuple2: second position
        :return: position between two given
        """
        diff = self.tuple_diff(tuple1, tuple2)
        if diff[0] == 2:
            return (tuple1[0] + 1, tuple1[1])
        elif diff[1] == 2:
            return (tuple1[0], tuple1[1] + 1)

    def positions_validation(self):
        """
        :return: True if LETTERS are on one line vertically or horizontally
        """
        positions_diff = list()
        for i in range(len(self.word) - 1):
            positions_diff.append(self.tuple_diff(self.word[i].position, self.word[i + 1].position))

        return self.is_horizontally(positions_diff) or self.is_vertically(positions_diff)

    def complete_word(self):
        """
        :return: word completed with one missing position
        """
        temp_positions = list()
        for i in range(1, len(self.word)):
            diff = self.tuple_diff(self.word[i - 1].position, self.word[i].position)
            if diff[0] == 2 or diff[1] == 2:
                position = self.find_missing_position(self.word[i - 1].position, self.word[i].position)
                letter = self.board.get_letter_from_position(position)

                if letter is not None:
                    temp_positions.append(MovingLetter(letter, position))

        self.word += temp_positions
        self.word = sorted(self.word, key=lambda word: word.position)

    def check_if_center(self):
        """
        :return: First word must go through (7, 7). Return true if indeed it does.
        """
        for i in self.word:
            if i.position == (7, 7):
                return True

        return False

    def create_list_of_words(self, word):
        """
        :param word: word with blank
        :return: list of all possible WORDS after replacing blank
        """
        result = list()
        choose = {
            'a': "aą",
            'c': "cć",
            'e': "eę",
            'l': "lł",
            'n': "nń",
            'o': "oó",
            's': "sś",
            'z': "zżź"
        }
        posibble_letters = choose.get(self.letter_under_blank, self.letter_under_blank)
        for i in posibble_letters:
            result.append(word.replace('?', i, 1))

        if word.count('?') == 2:
            temp_result = list()
            posibble_letters = choose.get(self.second_letter_under_blank, self.second_letter_under_blank)
            for i in result:
                for j in posibble_letters:
                    temp_result.append(i.replace('?', j))

            result += temp_result

        return result

    def word_plane(self):
        """
        :return: 'h' if letter is placed horizontally and 'v' when it is placed vertically
        """
        positions_diff = list()
        for i in range(len(self.word) - 1):
            positions_diff.append(self.tuple_diff(self.word[i].position, self.word[i + 1].position))

        if self.is_horizontally(positions_diff):
            return 'v'
        elif self.is_vertically(positions_diff):
            return 'h'

    def letter_positions(self):
        """
        :return: word's LETTERS' positions
        """
        pos = list()
        for i in self.word:
            pos.append(i.position)

        return pos

    def further_suffixes(self, pos, adder):
        """
        :param pos: start position
        :param adder: direction of searching
        :return: LETTERS for suffix
        """
        result = ''

        position = (pos[0] + adder[0], pos[1] + adder[1])

        next_letter = self.board.get_letter_from_position(position)

        if next_letter is None:
            if position in self.letter_positions():
                index = self.letter_positions().index(position)
                next_letter = self.word[index].letter

        while next_letter is not None:
            result += next_letter
            position = (position[0] + adder[0], position[1] + adder[1])
            next_letter = self.board.get_letter_from_position(position)
            if position in self.letter_positions():
                index = self.letter_positions().index(position)
                next_letter = self.collisions[index].letter

        return result

    def create_letter_under_blank(self, word):
        """
        :param word: word which was placed on BOARD
        :return: one letter which is represented on blank
        """
        for i in word:
            self.allowed_word = self.allowed_word.replace(i, '', 1)

    def word_suffixes_one_letter(self, recv_word):
        """
        :param recv_word: created word, one letter indeed
        :return: take suffixes for one-letter-long word
        """
        start_word_pos = self.word[0]
        stop_word_pos = self.word[-1]

        word = ''

        word_suffix = ''
        word_prefix = ''

        for i in self.collisions:
            if i.position[1] == start_word_pos.position[1] == stop_word_pos.position[1]:
                if i.position[0] < start_word_pos.position[0]:
                    word_prefix += i.letter
                    word_prefix += self.further_suffixes(i.position, [-1, 0])
                elif i.position[0] > stop_word_pos.position[0]:
                    word_suffix += i.letter
                    word_suffix += self.further_suffixes(i.position, [1, 0])

                if not self.check_new_word(word_prefix, word, recv_word, word_suffix):
                    return False

            elif i.position[0] == start_word_pos.position[0] == stop_word_pos.position[0]:
                if i.position[1] < start_word_pos.position[1]:
                    word_prefix += i.letter
                    word_prefix += self.further_suffixes(i.position, [0, -1])
                elif i.position[1] > stop_word_pos.position[1]:
                    word_suffix += i.letter
                    word_suffix += self.further_suffixes(i.position, [0, 1])

                if not self.check_new_word(word_prefix, word, recv_word, word_suffix):
                    return False

            word_suffix = ''
            word_prefix = ''
        return True

    def check_new_word(self, word_prefix, word, recv_word, word_suffix):
        """
        :param word_prefix:
        :param word:
        :param recv_word:
        :param word_suffix:
        :return: true if accidentally created word is correct
        """
        original_word = ''

        if word_prefix != "":
            word_prefix = word_prefix[::-1]

        word += word_prefix + recv_word + word_suffix

        if '?' in word:
            original_word = word
            word = self.create_list_of_words(word)

        if self.words_list.find_if_word_in_list(word)[0]:
            if original_word != '':
                self.allowed_word = self.words_list.find_if_word_in_list(word)[1]
                self.create_letter_under_blank(original_word)
            word = self.words_list.find_if_word_in_list(word)[1]
            self.created_words.append(word)
            self.created_word = word
            return True
        else:
            return False

    def word_suffixes(self, recv_word):
        """
        :param recv_word: word which is being created
        :return: True if suffixes and created word is correct
        """
        plane = self.word_plane()
        start_word_pos = self.word[0]
        stop_word_pos = self.word[-1]

        temp_collisions = list()

        word = ''

        word_suffix = ''
        word_prefix = ''

        if plane == 'v':
            for i in self.collisions:
                if i.position[1] == start_word_pos.position[1] == stop_word_pos.position[1]:
                    if i.position[0] < start_word_pos.position[0]:
                        word_prefix += i.letter
                        word_prefix += self.further_suffixes(i.position, [-1, 0])
                    elif i.position[0] > stop_word_pos.position[0]:
                        word_suffix += i.letter
                        word_suffix += self.further_suffixes(i.position, [1, 0])

                    temp_collisions.append(i)
                    if not self.check_new_word(word_prefix, word, recv_word, word_suffix):
                        return False

                word_suffix = ''
                word_prefix = ''

        elif plane == 'h':
            for i in self.collisions:
                if i.position[0] == start_word_pos.position[0] == stop_word_pos.position[0]:
                    if i.position[1] < start_word_pos.position[1]:
                        word_prefix += i.letter
                        word_prefix += self.further_suffixes(i.position, [0, -1])
                    elif i.position[1] > stop_word_pos.position[1]:
                        word_suffix += i.letter
                        word_suffix += self.further_suffixes(i.position, [0, 1])

                    temp_collisions.append(i)
                    if not self.check_new_word(word_prefix, word, recv_word, word_suffix):
                        return False

                word_suffix = ''
                word_prefix = ''

        for i in temp_collisions:
            self.collisions.remove(i)

        return True

    def random_created_word(self, recv_word):
        """
        :param recv_word: word which is being created
        :return: true if accidentally created word if correct
        """
        plane = self.word_plane()

        word = ''

        word_suffix = ''
        word_prefix = ''

        if plane == 'v':
            for colision in self.collisions:
                for letter in self.word:
                    if colision.position[0] == letter.position[0]:
                        found_letter = letter.letter
                        if colision.position[1] < letter.position[1]:
                            word_prefix += colision.letter
                            word_prefix += self.further_suffixes(colision.position, [0, -1])
                            word_suffix += self.further_suffixes(colision.position, [0, 1])
                        elif colision.position[1] > letter.position[1]:
                            word_suffix += colision.letter
                            word_suffix += self.further_suffixes(colision.position, [0, 1])
                            word_prefix += self.further_suffixes(colision.position, [0, -1])

                        if word_prefix == word_suffix == found_letter == '':
                            return True

                        if word_prefix != "":
                            word_prefix = word_prefix[::-1]

                        word = word_prefix + word_suffix

                        if not self.check_new_word('', word, '', ''):
                            return False

                word_suffix = ''
                word_prefix = ''

        elif plane == 'h':
            for colision in self.collisions:
                for letter in self.word:
                    if colision.position[1] == letter.position[1]:
                        found_letter = letter.letter
                        if colision.position[0] < letter.position[0]:
                            word_prefix += colision.letter
                            word_prefix += self.further_suffixes(colision.position, [-1, 0])
                            word_suffix += self.further_suffixes(colision.position, [1, 0])
                        elif colision.position[0] > letter.position[0]:
                            word_suffix += colision.letter
                            word_suffix += self.further_suffixes(colision.position, [1, 0])
                            word_prefix += self.further_suffixes(colision.position, [-1, 0])

                        if word_prefix == word_suffix == found_letter == '':
                            return True

                        if word_prefix != "":
                            word_prefix = word_prefix[::-1]

                        word = word_prefix + word_suffix

                        if not self.check_new_word('', word, '', ''):
                            return False

                word_suffix = ''
                word_prefix = ''

        if len(self.collisions) != 0:
            original_word = recv_word
            if '?' in recv_word:
                recv_word = self.create_list_of_words(recv_word)

                if not self.words_list.find_if_word_in_list(recv_word)[0]:
                    return False
                else:
                    recv_word = self.words_list.find_if_word_in_list(recv_word)[1]
                    self.allowed_word = self.words_list.find_if_word_in_list(recv_word)[1]
                    self.create_letter_under_blank(original_word)

        return True

    def validation(self):
        """
        :return: True if created word is in one line, is correct and all accidentally created WORDS are also correct
        """
        self.created_word = ''

        self.word = sorted(self.word, key=lambda word: word.position)

        # check first move
        if self.moves_counter == 0:  # first word must go through center
            word = ''
            original_word = ''
            for letter in self.word:
                word += letter.letter

            if '?' in word:
                original_word = word
                word = self.create_list_of_words(word)

            if not self.check_if_center():
                return False

            if not self.words_list.find_if_word_in_list(word)[0]:
                return False

            if not self.positions_validation():
                return False

            self.allowed_word = self.words_list.find_if_word_in_list(word)[1]
            self.create_letter_under_blank(original_word)

            return True

        else:  # next moves
            if len(self.word) >= 2:
                self.complete_word()

            if len(self.word) >= 2:
                if not self.positions_validation():
                    return False

            self.collisions = self.collision_validation()
            if len(self.collisions) == 0:
                return False

            word = ''
            for letter in self.word:
                word += letter.letter

            if len(self.word) == 1:
                if not self.word_suffixes_one_letter(word):
                    return False

                return True

            else:
                if not self.word_suffixes(word):
                    return False

                if self.created_word != '':
                    word = self.created_word

                if not self.random_created_word(word):
                    return False

                return True

    @staticmethod
    def check_range(position):
        """
        :param position: position to check if isn't  out of range
        :return: False if is out of range
        """
        x_coor = position[0]
        y_coor = position[1]

        return (0 <= x_coor < 15) and (0 <= y_coor < 15)

    def collision_validation(self):
        """
        :return: list of collisions which creating word can make
        """
        positions = [k.position for k in self.word]
        collisions = []
        for i in self.word:
            top = (i.position[0] - 1, i.position[1])
            down = (i.position[0] + 1, i.position[1])
            left = (i.position[0], i.position[1] - 1)
            right = (i.position[0], i.position[1] + 1)
            neighbours = [top, down, left, right]

            for j in neighbours:
                if self.check_range(j) and self.board.get_letter_from_position(j) is not None:
                    if j in positions:
                        continue
                    else:
                        temp = MovingLetter(self.board.get_letter_from_position(j), j)
                        collisions.append(temp)

        return collisions

    def put_word_on_board(self):
        """
        :return: put on BOARD new word
        """
        index = 0
        for i in self.word:
            if i.letter == '?':
                if len(self.allowed_word) == 2:
                    self.board.set_letter_on_position(i.position, self.allowed_word[index])
                    index += 1
                else:
                    self.board.set_letter_on_position(i.position, self.allowed_word)
            else:
                self.board.set_letter_on_position(i.position, i.letter)

    def change_player(self):
        """
        :return: next PLAYER on list becomes current playing one
        """
        self.current_playing_user = next(self.players)

    def remove_letter_from_word(self, letter):
        """
        :param letter: letter to remove from creating word
        :return: updated word, without given letter
        """
        for i in self.word:
            if i.letter == letter:
                self.word.remove(i)
                return

    def calculate_score(self):
        """
        :return: updated PLAYER's score with score for used tiles
        """
        print(self.created_words)
        print(self.word)
        score = 0
        word_factor = 1
        for i in self.word:
            if i.position in self.board.premium:
                premium = self.board.get_premium_from_position(i.position)
                if premium[0] == 'word':
                    word_factor *= premium[1]
                    score += self.letter_set.get_points(i.letter)
                elif premium[0] == 'letter':
                    score += self.letter_set.get_points(i.letter) * premium[1]
            else:
                score += self.letter_set.get_points(i.letter)

        if self.moves_counter == 0:
            word_factor *= 2

        score *= word_factor

        return score

    def end_move(self):
        """
        :return: end each single move: put word on BOARD, calculate score, change curret PLAYER, reset word
        """
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
            self.letter_under_blank = ''
            self.moves_counter += 1

            return True

    def pass_button_press(self):
        """
        :return: actions when pass_button was clicked: increment pass_amount
        """
        self.current_playing_user.increment_pass()
        return not self.check_pass()  # if false GAME stop

    def quit_button_press(self):
        """
        :return: actions when quit_button was clicked: return winner's NAME (in case of draw, winner is first PLAYER on a list)
        """
        scores = [i.score for i in self.players_list]
        names = [j.name for j in self.players_list]

        winner_score = max(scores)
        winner_name = names[scores.index(winner_score)]

        return (winner_name, winner_score)

    def check_pass(self):
        """
        :return: True if all PLAYERS clicked pass_button twice in row
        """
        pass_amounts = [i.amount_of_pass for i in self.players_list]
        return all(item >= 2 for item in pass_amounts)

    def check_type_of_field(self, pos):
        """
        :param pos: position to check if is on premium filed
        :return: premium if position is on it
        """
        if pos in self.board.premium:
            return self.board.get_premium_from_position(pos)
        else:
            return None

    def create_file_name(self, pos):
        """
        :param pos: position on BOARD to clear
        :return: file NAME of image to clear filed
        """
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
        """
        :param pos: position to take latter from word
        :return: letter on given position in word
        """
        for i in self.word:
            if i.position == pos:
                return i.letter

    def make_ai_move(self):
        """
        Call functions from AI Controller Module
        """
        self.word = self.controler_ai.make_move()
        clicked_positions = list()
        if self.word:
            self.put_word_on_board()
            self.current_playing_user.end_move_and_reset(self.calculate_score())

            self.letter_under_blank = ''
            self.moves_counter += 1

            for i in self.word:
                clicked_positions.append(i.position)

        return clicked_positions

    def stop_condition(self):
        """
        :return: False if there no LETTERS left and one holder is empty
        """
        if self.letter_set.number_of_letters == 0:
            for i in self.players_list:
                if len(i.holder) == 0:
                    return False

        return True
