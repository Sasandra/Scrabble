""" Module responsible for actions connected to tiles with letters. """
import collections
import random
import os

NamedLetter = collections.namedtuple('named_letter', 'amount points')

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
LETTERS_PATH = os.path.join(THIS_DIR, "letters.txt")


class Letters:
    """ Class responsible for storage and operations connected to letters tiles. """

    def __init__(self):
        self.letters = dict()
        self.number_of_letters = 100
        try:
            with open(LETTERS_PATH, 'r', encoding='utf-8') as reader:
                data = reader.read()
                data = data.replace('\n', "@")
                data = data.split('@')
                for line in data:
                    line = line.rstrip().split(':')
                    self.letters.update({line[0]: NamedLetter(int(line[1]), int(line[2]))})

        except IOError:
            print('Plik z literami nie został znaleziony.')

    def __iter__(self):
        return iter(self.letters)

    def __hash__(self):
        result = ''
        for word in self.letters:
            result = result + word + self.letters[word]
        return hash(result)

    def __getitem__(self, char):
        if char in self.letters:
            return self.letters[char]

    def __setitem__(self, char, value):
        self.letters[char] = value

    def get_amount(self, char):
        """
        :param char: Letter which amount we want to get.
        :return: Amount of given letter.
        """
        return int(self.letters[char].amount)

    def get_points(self, char):
        """
        :param char: Letter which points we want to get.
        :return: Points of given letter.
        """
        return int(self.letters[char].points)

    def decrement_amount(self, char):
        """
        :param char: Letter which amount will be decreased.
        """
        if self.get_amount(char) > 0:
            self.letters[char] = NamedLetter(self.get_amount(char) - 1, self.get_points(char))
            self.number_of_letters -= 1

    def random_letters(self, amount):
        """
        :param amount: amount of letter to random (max 7)
        :return: list of letters needed to complete player set
        """
        letters_to_return = list()
        while len(letters_to_return) < amount:
            letter = random.choice(list(self.letters.keys()))
            if self.get_amount(letter) > 0:
                self.decrement_amount(letter)
                letters_to_return.append(letter)
            if self.number_of_letters == 0:
                break

        return letters_to_return

    def increment_amount(self, char):
        """
        :param char: Letter which amount will be increased.
        """
        if self.number_of_letters < 101:
            self.letters[char] = NamedLetter(self.get_amount(char) + 1, self.get_points(char))
            self.number_of_letters += 1

    def change_letters(self, letters):
        """
        :param letters: list of letters to exchange
        :return: list of letters random from all available letters
        """
        letter_to_return = self.random_letters(len(letters))
        for i in letters:
            self.increment_amount(i)

        return letter_to_return
