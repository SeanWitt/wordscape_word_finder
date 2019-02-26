import unittest

from main import GameRunner


class GameRunnerTestCase(unittest.TestCase):

    def test__get_possible_sorted_letter_combinations(self):
        given_letters = 'abcd'
        game = GameRunner(given_letters)
        game._get_possible_sorted_letter_combinations()
        combos_found = game.sorted_letter_combinations
        expected_combinations = ['abc', 'abd', 'acd', 'bcd', 'abcd']
        self.assertEqual(combos_found, expected_combinations)

