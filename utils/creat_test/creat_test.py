class Test:
    def __init__(self, test_name, questions_quantity: int):
        self.default = {
            "test_name": test_name,
            "questions": []
        }
        self.questions_quantity = questions_quantity

    def create(self, text, answers):
        self.default["questions"].append(
                        {
                            "text": text,
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
