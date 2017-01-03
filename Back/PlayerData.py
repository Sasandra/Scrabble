""" Representation of one player"""
from Back.LettersSet import Letters


class Player:
    """Each player will have his/her own instance of this class"""
    def __init__(self, name):
        self.name = name
        self.letters_object = Letters()
        self.holder = self.letters_object.random_letters(7)
        self.score = 0

    def exchange_letter(self, letters):
        """
        :param letters: list of letters to exchange
        :return: holder with updated list of letters
        """
        exchanged = self.letters_object.change_letters(letters)
        for i in letters:
            self.holder.remove(i)

        for i in exchanged:
            self.holder.append(i)
