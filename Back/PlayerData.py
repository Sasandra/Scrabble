""" Representation of player"""
import copy


class Player:
    """Class to represent PLAYER data"""

    def __init__(self, name, letters_set_object):
        self.name = name
        self.letters_object = letters_set_object
        self.holder = self.letters_object.random_letters(7)
        self.score = 0
        self.amount_of_pass = 0
        self.if_change_letters = False

    def remove_double_clicked(self, letters):
        """
        :param letters: chosen LETTERS to exchange
        :return: list of LETTERS without double clicked
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
        :param letters: list of LETTERS to exchange
        :return: holder with updated list of LETTERS
        """
        if not self.if_change_letters:
            letters = self.remove_double_clicked(letters)
            exchanged = self.letters_object.change_letters(letters)
            for i in letters:
                self.holder.remove(i)

            for i in exchanged:
                self.holder.append(i)

            self.if_change_letters = False

    def complete_holder(self):
        """
        :return: fill holder with new random LETTERS
        """
        amount_of_lack_letters = 7 - len(self.holder)
        letters = self.letters_object.random_letters(amount_of_lack_letters)
        for i in letters:
            self.holder.append(i)

    def get_name(self):
        """
        :return: PLAYER's NAME
        """
        return self.name

    def update_score(self, new_scores):
        """
        :param new_scores:
        :return: add new_scores to PLAYER's score
        """
        self.score += new_scores

    def increment_pass(self):
        """
        :return: increment amount_of pass every time when PLAYER doesn't create a word
        """
        self.amount_of_pass += 1

    def end_move_and_reset(self, score):
        """
        :param score: score for created word
        :return: end move function: add score, fill holder, reset flags
        """
        self.amount_of_pass = 0
        self.if_change_letters = False
        self.update_score(score)
        self.complete_holder()

    def remove_letter_from_holder(self, letter):
        """
        :param letter: letter to remove from holder
        :return: holder without given letter
        """
        if letter in self.holder:
            self.holder.remove(letter)

    def return_letter_on_holder(self, letter):
        """
        :param letter: letter to put on holder
        :return: update holder with given letter
        """
        self.holder.append(letter)

    def swap_letter(self, letters):
        """
        :param letters: list of letter which was shifted
        :return: updated holder
        """
        self.holder = letters
