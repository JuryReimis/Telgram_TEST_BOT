from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNameTest(StatesGroup):
    Name_is_creating = State()
    Get_tests_length = State()
    Question_selection = State()
    Create_answers = State()
    Answer_became = State()
    Right_answer_became = State()
