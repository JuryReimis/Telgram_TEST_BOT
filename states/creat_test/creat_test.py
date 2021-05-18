from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNameTest(StatesGroup):
    Name_is_creating = State()
    Test_len = State()
    Question_create = State()
    Create_answers = State()
    Answer_became = State()
    Right_answer_became = State()
