""" Controller for AI Move"""

from collections import namedtuple
from Back import ComputerAI
from Back.Tree import Tree
from Back.Tree import Node

MovingLetter = namedtuple('MovingLetter', 'letter, position')


class AIController:
    """ Controller for AI Turn """

    def __init__(self, board, player, letter_set):
        self.computer_ai = ComputerAI.ComputerAI(player, letter_set)
        self.board = board
        self.places_on_board = list()

    @staticmethod
    def check_tuple(pair):
        """
        :param pair: tuple to check if contain zero
        :return: true if contains zero
        """
        for i in pair:
            if i == 0:
                return True

        return False

    @staticmethod
    def check_range(position):
        """
        :param position: position to check if isn't  out of range
        :return: False if is out of range
        """
        x_coor = position[0]
        y_coor = position[1]

        return (-1 <= x_coor <= 15) and (-1 <= y_coor <= 15)

    def find_empty_spaces_on_board(self):
        """
        find letter on BOARD where Ai can put the word
        """
        self.places_on_board = list()
        for row in range(15):
            for column in range(15):
                field = self.board.get_letter_from_position((row, column))

                if field is not None:
                    letter = MovingLetter(letter=field, position=(row, column))
                    row_range = self.row_space((row, column))
                    column_range = self.column_space((row, column))

                    if self.check_tuple(row_range):
                        row_range = [0, 0]

                    if self.check_tuple(column_range):
                        column_range = [0, 0]

                    if row_range == column_range == [0, 0]:
                        continue

                    self.places_on_board.append([letter, column_range, row_range])

    def row_space(self, pos):
        """
        :param pos: start position with letter to look for empty spaces around it in row
        :return: tuple: [empty fields on the left, empty fields on the right]
        """

        left_space = 0
        right_space = 0

        x_coor = pos[0]
        y_coor = pos[1]

        left_pos = x_coor - left_space - 1

        while 0 <= left_pos <= 14:
            if self.board.get_letter_from_position((left_pos, y_coor)) is None:
                if self.board.get_letter_from_position(
                        (left_pos, y_coor + 1)) is not None or self.board.get_letter_from_position(
                    (left_pos, y_coor - 1)) is not None:
                    break
                else:
                    left_space += 1
            elif left_space == 0:
                break
            else:
                left_space -= 1
                break

            left_pos = x_coor - left_space - 1

        right_pos = x_coor + right_space + 1

        while 0 <= right_pos <= 14:
            if self.board.get_letter_from_position((right_pos, y_coor)) is None:
                if self.board.get_letter_from_position(
                        (right_pos, y_coor + 1)) is not None or self.board.get_letter_from_position(
                    (right_pos, y_coor - 1)) is not None:
                    break
                else:
                    right_space += 1
            elif right_space == 0:
                break
            else:
                right_space -= 1
                break

            right_pos = x_coor + right_space + 1

        return [left_space, right_space]

    def column_space(self, pos):
        """
        :param pos: start position with letter to look for empty spaces around it in row
        :return: tuple: [empty fields on the left, empty fields on the right]
        """

        top_space = 0
        down_space = 0

        x_coor = pos[0]
        y_coor = pos[1]

        top_pos = y_coor - top_space - 1
        down_pos = y_coor + down_space + 1

        while 0 <= top_pos <= 14:
            if self.board.get_letter_from_position((x_coor, top_pos)) is None:
                if self.board.get_letter_from_position(
                        (x_coor + 1, top_pos)) is not None or self.board.get_letter_from_position(
                    (x_coor - 1, top_pos)) is not None:
                    break
                else:
                    top_space += 1
            elif top_space == 0:
                break
            else:
                top_space -= 1
                break

            top_pos = y_coor - top_space - 1

        while 0 <= down_pos <= 14:
            if self.board.get_letter_from_position((x_coor, down_pos)) is None:
                if self.board.get_letter_from_position(
                        (x_coor + 1, down_pos)) is not None or self.board.get_letter_from_position(
                    (x_coor - 1, down_pos)) is not None:
                    break
                else:
                    down_space += 1
            elif down_space == 0:
                break
            else:
                down_space -= 1
                break

            down_pos = y_coor + down_space + 1

        return [top_space, down_space]

    def check_if_blank(self):
        """
        :return: true if blank is in COMPUTER' holder, false otherwise
        """
        return '?' in self.computer_ai.player.holder

    def create_moving_word(self, word, direction, pos):
        """
        :param word: list of splited by letter from BOARD word's part
        :param direction: row or column
        :param pos: letter from BOARD position
        :return: list with MovingLetter word
        """
        prefix = word[0]
        suffix = word[2]

        moving_word = list()

        prefix_pos = suffix_pos = [pos[0], pos[1]]

        if direction == 'r':
            prefix_adder = [0, -1]
            suffix_adder = [0, 1]

        elif direction == 'c':
            prefix_adder = [-1, 0]
            suffix_adder = [1, 0]

        for i in range(len(prefix) - 1, -1, -1):
            prefix_pos = (prefix_pos[0] + prefix_adder[0], prefix_pos[1] + prefix_adder[1])
            moving_word.append(MovingLetter(letter=prefix[i], position=prefix_pos))
            self.computer_ai.player.remove_letter_from_holder(prefix[i])

        moving_word.reverse()

        for i in suffix:
            suffix_pos = (suffix_pos[0] + suffix_adder[0], suffix_pos[1] + suffix_adder[1])
            moving_word.append(MovingLetter(letter=i, position=suffix_pos))
            self.computer_ai.player.remove_letter_from_holder(i)

        return moving_word

    def make_move(self):
        """
        :return: word build with moving LETTERS
        """
        self.find_empty_spaces_on_board()

        move_info = self.computer_ai.find_move(self.places_on_board)

        i = 0
        while self.check_if_blank() and i <= 10:
            i += 1
            self.computer_ai.player.exchange_letter(['?'])

        if move_info:
            word = move_info[0][1]
            direction = move_info[1]
            letter_from_board_position = move_info[2]
            moving_word = self.create_moving_word(word, direction, letter_from_board_position)
            return moving_word

        else:
            self.computer_ai.player.exchange_letter(self.computer_ai.player.holder)
            self.computer_ai.player.amount_of_pass += 1
            return False
