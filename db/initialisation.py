# Скрипт для создания баз данных

import sqlite3


class TestsTable:
    def __init__(self, database):
        self.dir = "db/" + database
        self.conn = sqlite3.connect(database=self.dir)
        self.cur = self.conn.cursor()
        self.cur.row_factory = sqlite3.Row

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXiSTS questions(
        question_id INTEGER PRIMARY KEY AUTOINCREMENT ,
        test_name TEXT,
        question_text TEXT,
        answer_1 TEXT,
        answer_2 TEXT,
        answer_3 TEXT,
        answer_4 TEXT,
        FOREIGN KEY (test_name) REFERENCES tests(test_name)
        )""")

    def into_table(self, table, notes, right_answer: str = None):
        if table == "tests":
            self.cur.execute("""INSERT INTO tests(test_name, creater, questions, completed, visible) VALUES (?, ?, ?, ?, ?)""", notes)
        if table == "questions":
            self.cur.execute("""INSERT INTO questions(test_name, question_text, answer_1, answer_2, answer_3, answer_4) VALUES(?, ?, ?, ?, ?, ?)""", notes)
            #last_insert = self.cur.execute("""SELECT question_id FROM questions WHERE last_insert_rowid()""")
            self.save_table()
            self.select_all("questions", "question_id", self.cur.lastrowid)
            last_row = self.cur.fetchone()
            self.cur.execute("""INSERT INTO right_answers(question_id, right_answer) VALUES (?, ?)""", (last_row["question_id"], right_answer))
            self.save_table()

    def save_table(self):
        self.conn.commit()

    def del_table(self):
        self.cur.execute("""
        DROP TABLE IF EXISTS questions """)

    def select_all(self, table, param, note):
        context = f"""SELECT * FROM {table} WHERE {param} = ?"""
        self.cur.execute(context, (note, ))


if __name__ == "__main__":          #Для тестов
    tests = TestsTable("tests.sqlite3")
    tests.save_table()
    tests.select_all('tests', 'test_id', 1)
    print(tests.cur.fetchone()["test_id"])
    tests.cur.close()






# CREATE TABLE IF NOT EXISTS tests(
#     test_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
#     test_name TEXT,
#     creater TEXT,
#     questions INT,
#     completed INT,
#     visible NUMERIC
#     )
