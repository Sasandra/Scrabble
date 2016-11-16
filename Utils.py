"""Module with function to call"""
WORDS = {}


def read_words():
    """Read all allowable words in Scrabble"""
    words = {}
    with open('words.txt', mode='r', encoding='utf-8') as reader:
        for line in reader:
            line = line.rstrip()
            words[line] = 0
