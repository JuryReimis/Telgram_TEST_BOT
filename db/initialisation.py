# Скрипт для создания баз данных

import sqlite3


class TestsTable:
    def __init__(self, database):
        try:
            if __name__ == "__main__":
                self.dir = database
            else:
                self.dir = "db/" + database
            self.conn = sqlite3.connect(database=self.dir)
            self.conn.set_trace_callback(print)
            self.cur = self.conn.cursor()
            self.cur.row_factory = sqlite3.Row
        except:
            self.cur.close()
            print("Поймано исключение при инициализации бд")

    def create_table(self, table):
        if table == "tests":
            self.cur.execute("""CREATE TABLE IF NOT EXISTS tests(
            test_id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT,
            creater TEXT,
            questions INTEGER,
            completed INTEGER DEFAULT NULL,
            visible BLOB DEFAULT FALSE
             )""")
        if table == "questions":
            self.cur.execute("""CREATE TABLE IF NOT EXISTS questions(
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT,
            answer_1 TEXT,
            answer_2 TEXT,
            answer_3 TEXT,
            answer_4 TEXT
            )""")
        if table == "right_answers":
            self.cur.execute("""CREATE TABLE IF NOT EXISTS right_answers(
            question_id INTEGER,
            right_answer TEXT,
            FOREIGN KEY (question_id) REFERENCES questions(question_id) ON UPDATE CASCADE 
            )""")
        if table == "questions_in_tests":
            self.cur.execute("""CREATE TABLE IF NOT EXISTS questions_in_tests(
            test_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY (test_id) REFERENCES tests(test_id) ON UPDATE CASCADE 
            )""")

    def into_table(self, table, notes, right_answer: str = None):
        if table == "tests":
            self.cur.execute("""INSERT INTO tests(test_name, creater, questions, completed, visible) VALUES (?, ?, ?, ?, ?)""", notes)
            self.select_all("tests", "test_id", self.cur.lastrowid)
            self.test_id = self.cur.fetchone()["test_id"]
        if table == "questions":
            self.cur.execute("""INSERT INTO questions(test_name, question_text, answer_1, answer_2, answer_3, answer_4) VALUES(?, ?, ?, ?, ?, ?)""", notes)
            #last_insert = self.cur.execute("""SELECT question_id FROM questions WHERE last_insert_rowid()""")
            self.save_table()
            self.select_all("questions", "question_id", self.cur.lastrowid)
            last_row = self.cur.fetchone()
            self.cur.execute("""INSERT INTO right_answers(question_id, right_answer) VALUES (?, ?)""", (last_row["question_id"], right_answer))
            self.cur.execute("""INSERT INTO questions_in_tests(test_id, question_id) VALUES (?, ?)""", (self.test_id, last_row["question_id"]))
            self.save_table()

    def save_table(self):
        self.conn.commit()

    def del_table(self):
        self.cur.execute("""
        DROP TABLE IF EXISTS questions """)

    def select_all(self, table, param, note):
        context = f"""SELECT * FROM {table} WHERE {param} = ?"""
        self.cur.execute(context, (note, ))

    def create_temp_table(self):
        self.cur.execute("""CREATE TEMPORARY TABLE temp_1(
        parametr INTEGER)""")

    def select_random_str(self):
        context = f"""SELECT * FROM tests
        WHERE test_id NOT IN (SELECT * FROM temp)
        LIMIT 1 
        OFFSET ABS(RANDOM()) % MAX((SELECT COUNT(*) FROM tests), 1)
        """
        self.cur.execute(context)


class TemporaryTable:
    def __init__(self):
        try:
            self.con = sqlite3.connect("db/tests.sqlite3")
            self.con.set_trace_callback(print)
            self.cur = self.con.cursor()
            self.create_table()
        except:
            print("Ошибка создания временной бд")
            self.close_connection()

    def create_table(self):
        self.cur.execute("""CREATE TEMPORARY TABLE IF NOT EXISTS temp(
        param INTEGER)
        """)

    def into_table(self, param):
        self.cur.execute("""INSERT INTO temp(param) VALUES (?)""", param)

    def close_connection(self):
        self.cur.close()

if __name__ == "__main__":          #Для тестов
    tests = TestsTable("tests.sqlite3")
    tests.select_all("tests", "test_id", 15)
    tests.cur.close()
