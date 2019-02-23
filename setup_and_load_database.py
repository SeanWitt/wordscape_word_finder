import csv
import os
import sqlite3

from db_connection import WordsDatabaseConnection
from table_creator import TableCreator


INSERT_COMBO_SQL = "INSERT INTO letter_combinations (combination) VALUES (?)"
INSERT_RAW_WORD_SQL = "INSERT INTO raw_words (word, letter_combinations_id) VALUES (?,?)"
RETRIEVE_EXISTING_WORD_ID_SQL = "SELECT id FROM letter_combinations WHERE combination=?"

def remove_non_alphabet_characters(letters):
    """
    Removes every character that is non-alphabetic since the game does not use these.
    :param letters: String. Letters
    :return: String. Only letters, no special characters or numbers
    """
    letters = [l for l in letters if l.isalpha()]
    return "".join(letters)

def parse_file_to_load(word_db):
    """
    Parses a .txt file with all english words 

    :param word_db: Sql db object.

    :return: None
    """
    with open(word_db.word_list_filepath, 'rU') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            raw_word = remove_non_alphabet_characters(row[0])
            sorted_word = "".join(sorted(raw_word))
            letter_combination_id = insert_or_retrieve_combination(word_db, sorted_word)
            insert_raw_word(word_db, raw_word, letter_combination_id)
            status_printer(i)

def status_printer(i):
    """
    Prints status of the loading of word

    :param i: Integer. Index of loop

    :return: None
    """
    if i % 500 == 0:
        os.system("clear")
        print "Successfully Processed {} Words...".format(i)

def insert_or_retrieve_combination(word_db, sorted_word):
    """
    :param word_db: sql database object
    :param sorted_word: String. Letters of a raw word in alphabetical order

    :return: Integer. Row id of the inserted or retrieved letter combo
    """
    try:
        word_db.cursor.execute(INSERT_COMBO_SQL, (sorted_word,))
        word_db.conn.commit()
        row_id = word_db.cursor.lastrowid
    except sqlite3.IntegrityError:
        word_db.cursor.execute(RETRIEVE_EXISTING_WORD_ID_SQL, (sorted_word,))
        row_id = word_db.cursor.fetchall()[0][0]
    return row_id

def insert_raw_word(word_db, raw_word, combination_id):
    """
    :param word_db: sql database object
    :param raw_word: String. English word
    :param combination_id: Integer. Key of the sorted letter
    combination relating to raw_word from letter_combinations table

    :return: None
    """
    try:
        word_db.cursor.execute(INSERT_RAW_WORD_SQL, (raw_word, combination_id,))
        word_db.conn.commit()
    except sqlite3.IntegrityError:
        print("{} already exist in Words Database. Skipping".format(raw_word))

if __name__ == '__main__':
    path_to_words_file = 'allwords.txt'
    word_db = WordsDatabaseConnection.create()
    TableCreator(word_db)
    parse_file_to_load(word_db)

    