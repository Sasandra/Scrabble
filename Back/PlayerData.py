""" Representation of one player"""
from Back.LettersSet import Letters


class Player:
    """Each player will have his/her own instance of this class"""
    def __init__(self, name):
        self.name = name
        temp = Letters()
        self.holder = temp.random_letters(7)
