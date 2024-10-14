import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.cyk import CYK

class testCYK(unittest.TestCase):
    def setUp(self):
        self.grammar = {
            "variables": ["S0", "S", "U", "V", "A", "B"],
            "terminals": ["a", "b", "e"],
            "rules": [
                {"S0": ["UA", "VB", "a", "b", "e"]},
                {"S": ["UA", "VB", "a", "b"]},
                {"U": ["AS", "a"]},
                {"V": ["BS", "b"]},
                {"A": ["a"]},
                {"B": ["b"]}
            ]
        }
    
    def test_sentence_accepted(self):
        sentence = "abba"
        self.assertTrue(CYK(self.grammar, sentence))
        print("Test 'test_sentence_accepted' passed! Sentence 'abba' is accepted by the grammar.")
    
    def test_sentence_rejected(self):
        sentence = "abab"
        self.assertFalse(CYK(self.grammar, sentence))
        print("Test 'test_sentence_rejected' passed! Sentence 'abab' is rejected by the grammar.")
    
    def test_empty_sentence(self):
        sentence = ""
        self.assertFalse(CYK(self.grammar, sentence))
        print("Test 'test_empty_sentence' passed! Empty sentence is rejected by the grammar.")
    
    def test_single_terminal_accepted(self):
        # Cambiar la gramática para aceptar cadenas con solo un terminal
        self.grammar = {
            "variables": ["S"],
            "terminals": ["a", "b"],
            "rules": [
                {"S": ["a", "b"]}
            ]
        }
        sentence = "a"
        self.assertTrue(CYK(self.grammar, sentence))
        print("Test 'test_single_terminal_accepted' passed! Sentence 'a' is accepted by the grammar.")

    def test_single_terminal_rejected(self):
        sentence = "c"
        self.assertFalse(CYK(self.grammar, sentence))
        print("Test 'test_single_terminal_rejected' passed! Sentence 'c' is rejected by the grammar.")
        
if __name__ == '__main__':
    unittest.main()
    