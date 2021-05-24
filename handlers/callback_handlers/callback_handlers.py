import pprint

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from db.initialisation import TestsTable
from handlers.command_handlers.command_handlers import answer_became, create_questions
from keyboards.inline_keyboards.callback_datas import insult_callback, test_callback, create_right_answer_callback, \
    polling_callback
from main import dp

from states.creat_test.creat_test import CreateNameTest
from utils.creat_test.creat_test import Test


@dp.callback_query_handler(insult_callback.filter())
async def give_insult(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    if callback_data.get("insult_force") == str(1):
        await call.message.answer(text=f"Ну ладно, получай,{call.from_user.first_name}!\nТы разговариваешь, как просроченная колбоса")
    if callback_data.get("insult_force") == str(2):
        await call.message.answer(text=f"Хммм...\nНу ладно. Я думаю, что твое имя- {call.from_user.first_name}, означает отвратительный кожаный ублюдок!")
    if callback_data.get("insult_force") == str(3):
        await call.message.answer(text=f"Ах ты ублюдок кожаный, решил ко мне лезть, говно собачье, да я тебя сам сожру ублюдок вонючий...")
    print("Оскорбление выполнено")


@dp.callback_query_handler(text="cancel")
async def cancel_inline_keyboard(call: CallbackQuery):
    await call.message.answer(text="Сдался...")
    await call.answer(text=f"Ахаха, испугался, кожаный ублюдок, {call.from_user.first_name}!", show_alert=True) #show_alert- сообщение показывается как уведомление на экране
    await call.message.edit_reply_markup() #Закрывает инлайн клавиатуру


@dp.callback_query_handler(test_callback.filter())
async def test(call: CallbackQuery):
    await call.message.answer(text="OK")
    await call.message.edit_reply_markup()


@dp.callback_query_handler(create_right_answer_callback.filter(), state=CreateNameTest.Right_answer_became)
async def right_answer_selected(call: CallbackQuery, callback_data: dict, state: FSMContext):
    from handlers.command_handlers.command_handlers import iterations, test
    test.default["questions"][iterations-1]["answers"][int(callback_data["selected"])]["valid"] = True
    await call.message.edit_reply_markup()
    if iterations != test.questions_quantity:
        await call.message.answer(text=f"Введите {iterations + 1} вопрос")
        await CreateNameTest.Question_create.set()
    else:
        pprint.pprint(test.default)
        await create_questions(message=call.message, state=state)


@dp.callback_query_handler(polling_callback.filter(), state=CreateNameTest.Question_create)
async def created_question_accepted(call: CallbackQuery, callback_data: dict):
    if callback_data["selected"] is True:
        from handlers.command_handlers.command_handlers import test, iterations
        question_text = callback_data["context"]["question_text"]
        answers = [callback_data["context"]["answer_1"], callback_data["context"]["answer_2"], callback_data["context"]["answer_3"], callback_data["context"]["answer_4"]]
        database = TestsTable(database="tests.sqlite3")
        test.create(question_text, answers)
        for question in test.default["questions"][-1]["answers"]:
            database.select_all("right_answers", "right_answer", question["text"])
            if not database.cur.fetchone() is None:
                test.default["questions"][-1]["answers"][question]["valid"] = True





