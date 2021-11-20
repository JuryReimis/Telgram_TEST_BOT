from aiogram.dispatcher.filters.state import StatesGroup, State


class StartTest(StatesGroup):
    Test_choice = State()
    Test_started = State()
