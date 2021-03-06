from aiogram.utils.callback_data import CallbackData

r"""Список всех используемых CallbackData"""

insult_callback = CallbackData("insult", "insult_force")

test_callback = CallbackData("test_10q", "response")

test_menu_callback = CallbackData("test_menu", "choice")

selected_answer_callback = CallbackData("right_answer", "selected")

polling_callback = CallbackData("polling", "selected", "context")

select_test_callback = CallbackData("test_selected", "selected_id")
