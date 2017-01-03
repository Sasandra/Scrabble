""" Representation of one player"""
import copy
from Back.LettersSet import Letters


class Player:
    """Each player will have his/her own instance of this class"""
    def __init__(self, name):
        self.name = name
        self.letters_object = Letters()
        self.holder = self.letters_object.random_letters(7)
        self.score = 0

    def remove_double_clicked(self, letters):
        """
        :param letters: chosen letters to exchange
        :return: letters for exchange with removed these double clicked
        """
        holder_copy = copy.deepcopy(self.holder)
        letters_to_return = list()
        for i in letters:
            if i in holder_copy:
                letters_to_return.append(i)
                holder_copy.remove(i)
            else:
                continue

        return letters_to_return


    def exchange_letter(self, letters):
        """
        :param letters: list of letters to exchange
        :return: holder with updated list of letters
        """
        letters = self.remove_double_clicked(letters)
        exchanged = self.letters_object.change_letters(letters)
        for i in letters:
            self.holder.remove(i)

        for i in exchanged:
            self.holder.append(i)

    def get_name(self):
        """
        :return: player's name
        """
        return self.name

    def update_score(self, new_scores):
        """ add new_scores to player's score """
        self.score += new_scores
