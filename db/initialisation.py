# Скрипт для создания баз данных

import psycopg
from psycopg.rows import namedtuple_row
from config import USER_NAME_DB, DB_PASSWORD


class TestsTable:
    def __init__(self, database):
        try:
            self.dir = database
            self.con = psycopg.connect(dbname=self.dir, user=USER_NAME_DB, password=DB_PASSWORD,
                                       row_factory=namedtuple_row)
            self.curs = self.con.cursor()
            self.last_test_id = None
            self.create_table("tests")
            self.create_table("questions")
            self.create_table("right_answers")
            self.create_table("questions_in_tests")
            self.save_tables()
        except:
            if self.curs:
                self.curs.close()
            print("Поймано исключение при инициализации бд")

    def complete_execute(self, request, params=None, how_many="one"):
        result = self.con.execute(request, params)
        if how_many == "one":
            return result.fetchone()
        return result

    def create_table(self, table):
        if table == "tests":
            self.con.execute("""CREATE TABLE IF NOT EXISTS tests(
            test_id SERIAL PRIMARY KEY,
            test_name VARCHAR(50) NOT NULL ,
            creator VARCHAR(30) NOT NULL ,
            questions INTEGER NOT NULL ,
            completed INTEGER DEFAULT NULL,
            visible BOOLEAN DEFAULT FALSE 
             )""")  # visible - Булево значение
        if table == "questions":
            self.con.execute("""CREATE TABLE IF NOT EXISTS questions(
            question_id SERIAL PRIMARY KEY ,
            question_text TEXT NOT NULL ,
            answer_1 VARCHAR(50) NOT NULL ,
            answer_2 VARCHAR(50) NOT NULL ,
            answer_3 VARCHAR(50) NOT NULL ,
            answer_4 VARCHAR(50) NOT NULL 
            )""")
        if table == "right_answers":
            self.con.execute("""CREATE TABLE IF NOT EXISTS right_answers(
            question_id INTEGER,
            right_answer VARCHAR(50),
            FOREIGN KEY (question_id) REFERENCES tests.public.questions(question_id) ON UPDATE CASCADE ON DELETE CASCADE 
            )""")
        if table == "questions_in_tests":
            self.con.execute("""CREATE TABLE IF NOT EXISTS questions_in_tests(
            test_id INTEGER,
            question_id INTEGER,
            FOREIGN KEY (test_id) REFERENCES tests.public.tests(test_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES tests.public.questions(question_id) ON UPDATE CASCADE ON DELETE CASCADE 
            )""")

    def into_table(self, table, notes, right_answer: str = None):
        if table == "tests":
            self.con.execute(
                """INSERT INTO tests.public.tests(test_name, creator, questions, completed, visible)
                VALUES (%s, %s, %s, %s, %s)""",
                notes)
            self.last_test_id = self.last_insert_id("tests", "test_id")
            print(self.last_test_id)
        if table == "questions":
            self.con.execute(
                """INSERT INTO tests.public.questions(question_text, answer_1, answer_2, answer_3, answer_4)
                VALUES (%s, %s, %s, %s, %s)""",
                notes)
            self.con.execute("""INSERT INTO tests.public.right_answers(question_id, right_answer) VALUES (%s, %s)""",
                             (self.last_insert_id(table_name="questions", pk_name="question_id"), right_answer))
            self.con.execute("""INSERT INTO tests.public.questions_in_tests(test_id, question_id) VALUES (%s, %s)""",
                             (self.last_test_id, self.last_insert_id(table_name="questions", pk_name="question_id")))

    def add_preexisting_question_in_new_test(self, question_id):
        self.con.execute("""INSERT INTO tests.public.questions_in_tests(test_id, question_id) VALUES (%s, %s)""",
                         (self.last_test_id, question_id))

    def get_test(self, test_id):
        return self.con.execute("""SELECT test_name, questions FROM tests.public.tests WHERE test_id = %s""", (test_id,)).fetchone()

    def get_questions_for_test(self, test_id):
        question_ids = [i.question_id for i in
                        self.con.execute("""SELECT 
                        question_id 
                        FROM 
                        tests.public.questions_in_tests 
                        WHERE 
                        test_id = %s""", (test_id,)).fetchall()]
        return (self.con.execute(f"""SELECT * FROM tests.public.questions
        WHERE question_id IN {tuple(question_ids)}""").fetchall(),
                self.con.execute(
                    f"""SELECT * FROM tests.public.right_answers
                    WHERE question_id in{tuple(question_ids)}""").fetchall())

    def get_all_tests(self):
        return self.con.execute("""SELECT test_id, test_name FROM tests.public.tests""").fetchall()

    def save_tables(self):
        self.con.commit()

    def del_table(self):
        self.con.execute("""
        DROP TABLE IF EXISTS questions """)

    def select_all(self, table, param, note):
        context = f"""SELECT * FROM {"tests.public." + table} WHERE {param} = %s"""
        self.curs.execute(context, (note,))

    def last_insert_id(self, table_name, pk_name):
        sequence = f"{table_name}_{pk_name}_seq"
        return self.con.execute(f"SELECT * from {sequence}").fetchone().last_value


if __name__ == "__main__":  # Для тестов
    t = TestsTable("tests")
    notes = tuple([3, 4, 5])
    data = ('UK', 'France')
    sql = 'SELECT * from tests.public.questions WHERE questions.question_id IN %s'
    t.con.execute(sql, (data,))
    t.curs.close()
