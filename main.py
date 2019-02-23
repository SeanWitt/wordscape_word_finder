import os
import itertools

from db_connection import WordsDatabaseConnection

class GameRunner(object):

    def __init__(self, game_letters):
        self.game_letters = game_letters
        self.sorted_letter_combinations = []
        self.words_db = WordsDatabaseConnection.create()
        self.letter_combination_id_to_retrieve = []
        self.english_words_found = []

    def _get_possible_sorted_letter_combinations(self):
        """
        Get all possible alphabetized letter combinations
        at all lengths 
        """
        for i in range(3,len(self.game_letters)+1):
            sorted_combinations_at_this_length = itertools.combinations(self.game_letters, i)
            self._add_combinations_to_list(sorted_combinations_at_this_length)

    def _add_combinations_to_list(self, combination_generator):
        for combo in combination_generator:
            sorted_letter_combo = "".join(sorted(combo))
            self.sorted_letter_combinations.append(sorted_letter_combo)

    def _pull_ids_of_letter_combinations(self):
        for combo in self.sorted_letter_combinations:
            c_id = self.words_db.cursor.execute("SELECT id FROM letter_combinations WHERE combination=?", (combo,))
            fetched_id = c_id.fetchall()
            if len(fetched_id):
                self.letter_combination_id_to_retrieve.append(fetched_id[0][0])

    def pull_word_with_combination_id(self, combo):
        word = self.words_db.cursor.execute("SELECT word FROM raw_words WHERE letter_combinations_id=?", (combo,))
        self.english_words_found.append(word.fetchall()[0])

    def pretty_print_words(self, words_list):
        print words_list
        words_list.sort(lambda x,y: cmp(len(x), len(y)))
        for word in words_list:
            print word



if __name__ == '__main__':
    gr = GameRunner('pointblank')
    gr._get_possible_sorted_letter_combinations()
    gr._pull_ids_of_letter_combinations()
    for c_id in gr.letter_combination_id_to_retrieve:
        gr.pull_word_with_combination_id(c_id)
    gr.pretty_print_words(list(set(sum(gr.english_words_found, ()))))

            
