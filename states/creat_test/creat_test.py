from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNameTest(StatesGroup):
    NameIsCreating = State()
    Test_len = State()


class CreatQuestions(StatesGroup):
    def __init__(self, questions_quantity):
        classes = globals()
        for i in range(questions_quantity):
            name = f"State_{i+1}"
            classes[name] = State()
