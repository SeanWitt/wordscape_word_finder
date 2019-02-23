class TableCreator(object):
    """
    Creates database tables
    """

    def __init__(self, db_conn):
        self.db_conn = db_conn
        word_combinations_create_string = """
            CREATE TABLE IF NOT EXISTS letter_combinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            combination VARCHAR(26) UNIQUE
            );
        """
        raw_word_create_string = """
            CREATE TABLE IF NOT EXISTS raw_words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word VARCHAR(48) UNIQUE,
                letter_combinations_id INTEGER,
                FOREIGN KEY(letter_combinations_id) REFERENCES letter_combinations(id)
            );
        """
        self.create_table(word_combinations_create_string)
        self.create_table(raw_word_create_string)


    def create_table(self, create_statement):
        """
        Creates database table with given SQL formatted string

        :param cursor: Curser Object for SQL
        :param create_statement: String. Formatted string to create table for SQL

        :return: None
        """
        self.db_conn.cursor.execute(create_statement)
