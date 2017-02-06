""" Implementation of Tree """

from copy import deepcopy
from Back import WordsList

WORDS = WordsList.Words()
WORDS_SET = set(WORDS)


class Node:
    """ Tree's node """

    def __init__(self, value, parent_word):
        self.value = value
        self.children = []
        self.word = parent_word + self.value
        self.is_word = self.check_if_allowed(self.word)

    def add_child(self, letter):
        """
        :param letter: letter to add to node's children
        :return: updated node's children
        """
        self.children.append(letter)

    def if_already_exists(self, word):
        """
        :param word: word to check if its first letter is equal to current node child
        :return: child if true, false otherwise
        """

        for child in self.children:
            if child.value == word[0]:
                return child

        return False

    def add_word(self, word):
        """
        :param word: word to add to tree
        :return: updated tree with given word
        """
        if len(word) == 0:
            return False

        temp = Node(word[0], self.word)
        child_words = {c.word: c for c in self.children}

        if temp.word not in child_words:
            self.add_child(temp)
        else:
            temp = child_words[temp.word]

        word = word[1:]

        temp.add_word(word)

    @staticmethod
    def check_if_allowed(word):
        """
        :param word: word to check if is allowed in GAME
        :return: true if is allowed false otherwise
        """
        return word in WORDS_SET

    def find_all_words(self, letters):
        """
        :param letters: letter to find all possible WORDS
        :return: list of possible WORDS to create
        """
        possible_words = []
        if self.is_word:
            possible_words.append(self.word)

        for char in self.children:
            if char.value in letters:
                remaining_letters = self.change_letters(char.value, letters)
                possible_words.extend(char.find_all_words(remaining_letters))

        return possible_words

    @staticmethod
    def change_letters(value, letters):
        """
        :param value: letter to remove from LETTERS
        :param letters: list of letter to update
        :return: LETTERS without value
        """
        letters = deepcopy(letters)
        letters.remove(value)
        remaining_letters = letters

        return remaining_letters


class Tree:
    """ representation of Tree """

    def __init__(self, root):
        self.root = root

    def create_tree_from_words(self, words):
        """
        create tree from WORDS from GAME's dictionary
        """
        for word in words:
            self.root.add_word(word)

    def find_all_words(self, letters):
        """
        :param letters: LETTERS to find WORDS
        :return: all possible WORDS from given letter
        """
        return self.root.find_all_words(letters)
