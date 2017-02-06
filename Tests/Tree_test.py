""" Testing Tree module"""
import unittest
from Back import Tree


class TreeTest(unittest.TestCase):
    def setUp(self):
        self.root = Tree.Node('', '')
        self.tree = Tree.Tree(self.root)
        self.tree.create_tree_from_words(['mat', 'mam', 'mar'])

    def test_find_all_words(self):
        letters = ['m', 'a', 'r']
        result = self.tree.find_all_words(letters)
        self.assertEqual(result, ['ma', 'mar'])


suite = unittest.TestLoader().loadTestsFromTestCase(TreeTest)
print(unittest.TextTestRunner(verbosity=3).run(suite))
