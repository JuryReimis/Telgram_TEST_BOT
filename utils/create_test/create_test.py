class Test:
    def __init__(self, test_name: str, questions_quantity: int):
        self.test_structure = {
            "test_name": test_name,
            "questions": []
        }
        self.questions_quantity = questions_quantity

    def create(self, question_text, answers):
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

    def get_questions(self):
        return self.test_structure["questions"]
