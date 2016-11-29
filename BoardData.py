""" Module responsible for storage data about board and method connected to actions on board."""
import collections

Premium = collections.namedtuple('premium', 'kind factor')


class BoardData:
    """
    Class which represent board
    """
    def __init__(self):
        self.__board = collections.OrderedDict()
        self.__premium = collections.OrderedDict()
        for i in range(15):
            for j in range(15):
                self.__board.update({(j, i): None})

        self.read_premium()

    def read_premium(self):
        """
        :return: read data about premiums from file
        """
        try:
            with open('premia.txt', 'r', encoding='utf-8') as reader:
                for i in reader:
                    i = i.rstrip().replace('(', '').replace(')', '')
                    pairs = i.split(':')
                    premium_data = pairs[1].split(',')
                    premium_data = Premium(premium_data[0], int(premium_data[1]))
                    coord = pairs[0].split(',')
                    self.__premium.update({(int(coord[0]), int(coord[1])): premium_data})
        except IOError:
            print('Plik z premiami nie został znaleziony.')

    def __hash__(self):
        result = ''
        for word in self.__board:
            result = result + word + self.__board[word]
        return hash(result)

    def get_letter_from_position(self, position):
        """
        :param position: position from which we want to get letter
        :return: letter from given position
        """
        if position in self.__board:
            return self.__board[position]

    def set_letter_on_position(self, position, letter):
        """
        :param position: position on which we want to set given letter
        :param letter: letter to set on position
        """
        if position in self.__board:
            self.__board[position] = letter

    def get_premium_from_position(self, position):
        """
        :param position: tuple - position from wich we want to take premium
        :return: type Premium
        """
        if not isinstance(position, tuple):
            position = tuple(position)
        if position in self.__premium:
            return self.__premium[position].factor
