r"""Здесь происходит все взаимодействие с базой данных"""

import psycopg
from psycopg.rows import namedtuple_row
from config import USER_NAME_DB, DB_PASSWORD


class TestsTable:
    r"""При создании экземпляра этого класса происходит подключение к базе данных со своим курсором.
    Служит для взаимодействия с базой данных каждого модуля, независимо от других"""

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
        except Exception:
            if self.curs:
                self.curs.close()
            print("Поймано исключение при инициализации бд")

    def create_table(self, table):
        r"""Метод проверяет наличие необходимых для викторины таблиц, если они не созданы,
         то происходит создание и реализация всех связей.
         Если метод получает в аргументе tests происходит создание таблицы с таким названием в подключенной базе данных.
         Если аргумент questions, то происходит создание таблицы с таким названием.
         Если аргумент right_answers, то создается таблицы, при этом внешним ключем становится идентификатор из таблицы
         questions.
         Если аргумент questions_in_tests, то создается таблица, в которой внешними ключами являются сразу два значения-
         это идентификаторы из tests и questions"""
        if table == "tests":
            self.con.execute("""CREATE TABLE IF NOT EXISTS tests(
            test_id SERIAL PRIMARY KEY,
            test_name VARCHAR(50) NOT NULL ,
            creator VARCHAR(30) NOT NULL ,
            questions INTEGER NOT NULL ,
            completed INTEGER DEFAULT NULL,
            visible BOOLEAN DEFAULT FALSE 
             )""")
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

    def into_table(self, table: str, notes: list or tuple, right_answer: str = None):
        r"""Метод нужен для добавления в таблицы необходимых данных
        в table передается название таблицы, в notes данные, которые нужно записать в таблицу, right_answer-ситуативный
        аргумент, передается только если записываем в таблицу questions
        При записи в questions автоматически происходит запись в right_answers и в questions_in_tests"""
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
        r"""Метод для добавления уже существующего вопроса в создаваемый тест
        Берет идентификатор вопроса, который передается в аргумент и записывает еще строчку в questions_in_tests"""
        self.con.execute("""INSERT INTO tests.public.questions_in_tests(test_id, question_id) VALUES (%s, %s)""",
                         (self.last_test_id, question_id))

    def get_test(self, test_id):
        r"""Метод возвращает текст вопроса и ответы на него по заданному идентификатору вопроса"""
        return self.con.execute("""SELECT test_name, questions 
            FROM tests.public.tests 
            WHERE test_id = %s""", (test_id,)).fetchone()

    def get_questions_for_test(self, test_id):
        r"""Метод возвращает все вопросы, которые связаны с идентификатором теста, который передан в аргумент"""
        question_ids = [i.question_id for i in
                        self.con.execute("""SELECT question_id 
                            FROM tests.public.questions_in_tests 
                            WHERE test_id = %s""", (test_id,)).fetchall()]
        return (self.con.execute(f"""SELECT * 
            FROM tests.public.questions
            WHERE question_id 
            IN {tuple(question_ids)}""").fetchall(),
                self.con.execute(
                    f"""SELECT * FROM tests.public.right_answers
                    WHERE question_id in{tuple(question_ids)}""").fetchall())

    def get_all_tests(self):
        r"""Метод возвращает название и идентификатор всех присутствующих в базе тестов"""
        return self.con.execute("""SELECT test_id, test_name FROM tests.public.tests""").fetchall()

    def update_completed_number(self, test_id):
        r"""Метод обновляет количество раз, которые был пройден тест, вызывается после прохождения теста"""
        completed = int(self.con.execute("""SELECT completed 
            FROM tests.public.tests 
            WHERE test_id = %s""", (test_id,)).fetchone()[0])
        self.con.execute("""UPDATE tests.public.tests SET completed = %s WHERE test_id = %s""",
                         (completed + 1, test_id))

    def save_tables(self):
        r"""Метод завершает транзакцию, сохраняет все таблицы"""
        self.con.commit()

    def select_all(self, table, param, note):
        r"""Метод, который передает курсору все из таблицы table, где param равен note
        Служит для получения доступа к выборкам из БД по определенному параметру"""
        context = f"""SELECT * 
            FROM {"tests.public." + table} 
            WHERE {param} = %s"""
        self.curs.execute(context, (note,))

    def last_insert_id(self, table_name, pk_name):
        r"""Метод возвращает последний записанный в БД идентификатор"""
        sequence = f"{table_name}_{pk_name}_seq"
        return self.con.execute(f"""SELECT * 
            FROM {sequence}""").fetchone().last_value


if __name__ == "__main__":  # Для проверок
    t = TestsTable("tests")
    data = ('UK', 'France')
    sql = 'SELECT * from tests.public.questions WHERE questions.question_id IN %s'
    t.con.execute(sql, (data,))
    t.curs.close()
