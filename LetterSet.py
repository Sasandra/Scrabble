""" Module responsible for actions with tiles with letters. """
import collections

NamedLetter = collections.namedtuple('named_letter', 'amount points')


class LetterSet:
    """ Class responsbile for storage and operations connected to letters tiles. """
    def __init__(self):
        self.__letters = dict()
        try:
            with open('letters.txt', 'r') as reader:
                data = reader.read()
                data = data.replace('\n', "@")
                data = data.split('@')
                for line in data:
                    line = line.rstrip().split(':')
                    self.__letters.update({line[0]: NamedLetter(int(line[1]), int(line[2]))})

        except IOError:
            print('Plik z literami nie został znaleziony.')

    def __iter__(self):
        return iter(self.__letters)

    def __hash__(self):
        result = ''
        for word in self.__letters:
            result = result + word + self.__letters[word]
        return hash(result)

    def __getitem__(self, char):
        if char in self.__letters:
            return self.__letters[char]

    def __setitem__(self, char, value):
        self.__letters[char] = value

    def get_amount(self, char):
        """
        :param char: Letter which amount we want to get.
        :return: Amount of given letter.
        """
        return int(self.__letters[char].amount)

    def get_points(self, char):
        """
        :param char: Letter which amount we want to get.
        :return: Points of given letter.
        """
        return int(self.__letters[char].points)

    def dekrement_amount(self, char):
        """
        :param char: Letter which amount we want to decrease.
        """
        if self.get_amount(char) > 0:
            self.__letters[char] = NamedLetter(self.get_amount(char)-1, self.get_points(char))
