class Test:
    def __init__(self, test_name, questions_quantity: int):
        self.default = {
            "test_name": test_name,
            "questions": []
        }
        self.questions_quantity = questions_quantity


    def creat(self, text, answers):
        self.default["questions"].append(
                        {
                            "text": text,
                            "answers": [
                                {
                                    "text": "",
                                    "valid": False
                                },
                                {
                                    "text": "",
                                    "valid": False
                                },
                                {
                                    "text": "",
                                    "valid": False
                                },
                                {
                                    "text": "",
                                    "valid": False
                                }
                            ]
                        }
        )