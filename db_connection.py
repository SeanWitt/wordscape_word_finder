import os
import sqlite3

class WordsDatabaseConnection(object):

    def __init__(self, db_filepath, word_list_filepath):
        """
        :param db_filepath: String. Path to database
        :param word_list_filepath: String. Path to file with all english words
        """
        self.word_list_filepath = word_list_filepath
        self.conn = self._create_connection(db_filepath)
        self.cursor = self.conn.cursor()

    def _create_connection(self, database_file):
        """
        Creates a connection to the words database
        """
        try:
            conn = sqlite3.connect(database_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def __del__(self):
        """
        Close Connection
        """
        self.conn.close()
    
    @classmethod
    def create(cls):
        """
        Creates a cls object with default values
        """
        default_database = "{}/all_english_words.db".format(os.getcwd())
        default_word_text_file_path = 'allwords.txt'
        return cls(
            default_database, 
            default_word_text_file_path
        )