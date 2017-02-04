""" Module for storage data about allowed words and method connected to actions with words."""
import os

THIS_DIR, THIS_FILENAME = os.path.split(__file__)
WORDS_PATH = os.path.join(THIS_DIR, "words.txt")


class Words:
    """ Class which represent list of all allowed words in the game """

    def __init__(self):
        self.words = list()
        self.used_words = list()
        try:
            with open(WORDS_PATH, mode='r', encoding='utf-8') as reader:
                for line in reader:
                    line = line.rstrip()
                    self.words.append(line)
        except IOError:
            print('Plik ze słowami nie został znaleziony.')

    def __iter__(self):
        return iter(self.words)

    def __hash__(self):
        result = ''
        for word in self.words:
            result += word
        return hash(result)

    def add_used_word(self, word):
        """
        :param word: word to put on used_words list
        """
        self.used_words.append(word)

    def find_if_word_in_used_list(self, word):
        """
        :param word: word to chcek if it is in used_words_list
        :return: true if is, false if not
        """
        return word in self.used_words

    def find_if_word_in_list(self, word):
        """
        :param word: word which is being looked in game's dictionary
        :return: True when given word is allowed or False when it isn't
        """
        if isinstance(word, str):
            return word in self.words, word

        for i in word:
            if i in self.words:
                return True, i
        return False, None
