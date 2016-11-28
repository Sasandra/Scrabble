""" Module responsible for storage data about board and method connected to actions on board."""
import collections


class BoardData:
    """
    Class which represent board
    """
    def __init__(self):
        self.board = collections.OrderedDict()
        self.__premium = dict()
        for i in range(15):
            for j in range(15):
                self.board.update({(j, i): None})

    def __hash__(self):
        result = ''
        for word in self.board:
            result = result + word + self.board[word]
        return hash(result)

    def get_letter_from_position(self, position):
        """
        :param position: position from which we want to get letter
        :return: letter from given position
        """
        if position in self.board:
            return self.board[position]

    def set_letter_on_position(self, position, letter):
        """
        :param position: position on which we want to set given letter
        :param letter: letter to set on position
        """
        if position in self.board:
            self.board[position] = letter
