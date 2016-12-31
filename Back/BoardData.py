""" Module responsible for storage data about board and method connected to actions on board."""
import collections
import pygame

Premium = collections.namedtuple('premium', 'kind factor')


class Board:
    """
    Class which represent board
    """
    def __init__(self):
        self.board = collections.OrderedDict()
        self.premium = collections.OrderedDict()
        self.fields = collections.OrderedDict()
        for i in range(15):
            for j in range(15):
                self.board.update({(i, j): None})

        self.read_premium()
        self.read_coordinates()

    def read_premium(self):
        """
        :return: read data about premiums from file
        """
        try:
            with open('Back\\premia.txt', 'r', encoding='utf-8') as reader:
                for i in reader:
                    i = i.rstrip().replace('(', '').replace(')', '')
                    pairs = i.split(':')
                    premium_data = pairs[1].split(',')
                    premium_data = Premium(premium_data[0], int(premium_data[1]))
                    coord = pairs[0].split(',')
                    self.premium.update({(int(coord[0]), int(coord[1])): premium_data})
        except IOError:
            print('Plik z premiami nie został znaleziony.')

    def read_coordinates(self):
        """
        :return: read fields' coordinates on screen
        """
        rectangles = list()
        counter = 0
        try:
            with open('Back\\board_grid', 'r') as r:
                data = r.readlines()
                for i in data:
                    if '#' in i:
                        continue
                    i = i.rstrip()
                    x_y = i.split(',')
                    coor = list()
                    for j in x_y:
                        j = j.strip(' ')
                        coor.append(j)
                    rect = pygame.Rect(float(coor[0]), float(coor[1]), float(coor[2]), float(coor[3]))
                    rectangles.append(rect)

                for i in range(15):
                    for j in range(15):
                        self.fields.update({(i, j): rectangles[counter]})
                        counter += 1

        except IOError:
            print('Plik z współrzędnymi nie został znaleziony.')


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

    def get_premium_from_position(self, position):
        """
        :param position: tuple - position from wich we want to take premium
        :return: type Premium
        """
        if not isinstance(position, tuple):
            position = tuple(position)
        if position in self.premium:
            return self.premium[position].factor
