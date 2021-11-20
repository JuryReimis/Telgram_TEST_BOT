# Скрипт для создания баз данных

import sqlite3


class TestsTable:
    def __init__(self, database):
        try:
            if __name__ == "__main__":
                self.dir = database
            else:
                self.dir = "db/" + database
            self.con = sqlite3.connect(database=self.dir)
            self.con.set_trace_callback(print)
            self.curs = self.con.cursor()
            self.test_id = None
            self.con.execute("""PRAGMA foreign_keys = ON""")
            self.curs.row_factory = sqlite3.Row
        except:
            self.curs.close()
            print("Поймано исключение при инициализации бд")

    def create_table(self, table):
        if table == "tests":
            self.curs.execute("""CREATE TABLE IF NOT EXISTS tests(
            test_id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT,
            creater TEXT,
            questions INTEGER,
            completed INTEGER DEFAULT NULL,
            visible INTEGER DEFAULT 0 
             )""")  # visible - Булево значение
        if table == "questions":
            self.curs.execute("""CREATE TABLE IF NOT EXISTS questions(
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT,
            answer_1 TEXT,
            answer_2 TEXT,
            answer_3 TEXT,
            answer_4 TEXT
            )""")
        if table == "right_answers":
            self.curs.execute("""CREATE TABLE IF NOT EXISTS right_answers(
            question_id INTEGER,
            right_answer TEXT,
            FOREIGN KEY (question_id) REFERENCES questions(question_id) ON UPDATE CASCADE ON DELETE CASCADE 
            )""")
        if table == "questions_in_tests":
            self.curs.execute("""CREATE TABLE IF NOT EXISTS questions_in_tests(
            test_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY (test_id) REFERENCES tests(test_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(question_id) ON UPDATE CASCADE ON DELETE CASCADE 
            )""")

    def into_table(self, table, notes, right_answer: str = None):
        if table == "tests":
            self.curs.execute(
                """INSERT INTO tests(test_name, creater, questions, completed, visible) VALUES (?, ?, ?, ?, ?)""",
                notes)
            self.select_all("tests", "test_id", self.curs.lastrowid)
            self.test_id = self.curs.fetchone()["test_id"]
        if table == "questions":
            self.curs.execute(
                """INSERT INTO questions(question_text, answer_1, answer_2, answer_3, answer_4) VALUES (?, ?, ?, ?, ?)""",
                notes)
            self.select_all("questions", "question_id", self.curs.lastrowid)
            last_row = self.curs.fetchone()
            self.curs.execute("""INSERT INTO right_answers(question_id, right_answer) VALUES (?, ?)""",
                              (last_row["question_id"], right_answer))
            self.curs.execute("""INSERT INTO questions_in_tests(test_id, question_id) VALUES (?, ?)""",
                              (self.test_id, last_row["question_id"]))

    def add_preexisting_question_in_new_test(self, question_id):
        self.curs.execute("""INSERT INTO questions_in_tests(test_id, question_id) VALUES (?, ?)""",
                          (self.test_id, question_id))

    def get_all_tests(self):
        return self.curs.execute("""SELECT test_id, test_name FROM tests""").fetchall()

    def save_tables(self):
        self.con.commit()

    def del_table(self):
        self.curs.execute("""
        DROP TABLE IF EXISTS questions """)

    def select_all(self, table, param, note):
        context = f"""SELECT * FROM {table} WHERE {param} = ?"""
        self.curs.execute(context, (note,))

    def create_temp_table(self):
        self.curs.execute("""CREATE TEMPORARY TABLE temp_1(
        parametr INTEGER)""")


if __name__ == "__main__":  # Для тестов
    tests = TestsTable("tests.sqlite3")
    tests.con.commit()
    tests.curs.close()
