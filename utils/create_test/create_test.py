r"""Утилита для создания 'скелета' теста со своей структурой"""


class Test:
    def __init__(self, test_name: str = None, questions_quantity: int = None):
        r"""При создании экземпляра класса создаются структура, количество вопросов и словарь для ответов ползователя,
        по-умолчанию-пустой"""
        self.test_structure = {
            "test_name": test_name,
            "questions": []
        }
        self.questions_quantity = questions_quantity
        self.user_answers: dict = {}

    def create(self, question_text: str, answers: list):
        r"""Метод позволяет добавить очередной вопрос в структуру
        в метод передается текст вопроса и список ответов"""
        self.test_structure["questions"].append(
            {
                "text": question_text,
                "answers": [
                    {
                        "text": answers[0],
                        "valid": False
                    },
                    {
                        "text": answers[1],
                        "valid": False
                    },
                    {
                        "text": answers[2],
                        "valid": False
                    },
                    {
                        "text": answers[3],
                        "valid": False
                    }
                ]
            }
        )

    def test_from_db(self, questions: list, right_answers: list):
        """В этот метод будут подаваться два списка, полученные из БД
        В первом будут все вопросы, удовлетворяющие id, выбранного теста
        Во втором все правильные ответы к этому тесту
        Сначала будет сформирован словарь, где ключами будут id вопросов, а значениями правильные ответы
        После путем перебора всех вопросов из списка будет сформирована структура теста, без имени (оно не несет
        никакого смысла на этом этапе, но со всеми упорядоченными вопросами и ответами)"""
        valid = {}
        for answer in right_answers:
            valid[answer.question_id] = answer.right_answer
        for question in questions:
            self.test_structure["questions"].append({"text": question.question_text,
                                                     "answers": [
                                                         {
                                                             "text": question.answer_1,
                                                             "valid": True if valid[
                                                                                  question.question_id] == question.answer_1 else False
                                                         },
                                                         {
                                                             "text": question.answer_2,
                                                             "valid": True if valid[
                                                                                  question.question_id] == question.answer_2 else False
                                                         },
                                                         {
                                                             "text": question.answer_3,
                                                             "valid": True if valid[
                                                                                  question.question_id] == question.answer_3 else False
                                                         },
                                                         {
                                                             "text": question.answer_4,
                                                             "valid": True if valid[
                                                                                  question.question_id] == question.answer_4 else False
                                                         }
                                                     ], })
        return self.test_structure

    def create_users_answers(self, question: str, question_index: int, answer: int):
        r"""При выборе ответа во время провидения викторины через эту функцию создается словарь, где ключем является
         вопрос, а значением-ответ пользователя"""
        self.user_answers[question] = self.test_structure["questions"][question_index]["answers"][answer]["text"]

    def get_questions(self):
        r"""Возвращает список вопросов"""
        return self.test_structure["questions"]
