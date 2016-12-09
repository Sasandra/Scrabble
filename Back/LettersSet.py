""" Module responsible for actions with tiles with letters. """
import collections
import random

NamedLetter = collections.namedtuple('named_letter', 'amount points')


class Letters:
    """ Class responsbile for storage and operations connected to letters tiles. """
    def __init__(self):
        self.__letters = dict()
        self.__number_of_letters = 100
        try:
            with open('Back/letters.txt', 'r') as reader:
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
            self.__number_of_letters -= 1

    def random_letters(self, amount):
        """
        :param amount: ammount of letter to random (max 7)
        :return: list of letter which we need to complete player set
        """
        letters_to_return = list()
        while len(letters_to_return) < amount:
            letter = random.choice(list(self.__letters.keys()))
            if self.get_amount(letter) > 0:
                self.dekrement_amount(letter)
                letters_to_return.append(letter)
            if self.__number_of_letters == 0:
                break

        return letters_to_return

    def increment_amount(self, char):
        """
        :param char: Letter which amount we want to increase.
        """
        if self.__number_of_letters < 101:
            self.__letters[char] = NamedLetter(self.get_amount(char)+1, self.get_points(char))
            self.__number_of_letters += 1


    def change_letters(self, letters):
        """
        :param letters: list of letter we want to exchange
        :return: list of letters random from all avalible letters
        """
        letter_to_return = self.random_letters(len(letters))
        for i in letters:
            self.increment_amount(i)
            print(i)

        return letter_to_return
