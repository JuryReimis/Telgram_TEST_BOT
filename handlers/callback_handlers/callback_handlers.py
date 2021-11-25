import pprint

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from db.initialisation import TestsTable
from handlers.command_handlers.command_handlers import TestCreator, TestShower
from keyboards.default import menu
from keyboards.inline_keyboards import choice_right_answer_in_test
from keyboards.inline_keyboards.callback_datas import insult_callback, test_callback, selected_answer_callback, \
    polling_callback, test_menu_callback, select_test_callback
from keyboards.inline_keyboards.choice_right_answer_in_test import choice_answer_menu
from main import dp
from states.creat_test.creat_test import CreateNameTest
from states.start_test.start_test import StartTest
from utils.create_test.create_test import Test
from utils.test_selection.test_selection import output_question


@dp.callback_query_handler(insult_callback.filter())
async def give_insult(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    if callback_data.get("insult_force") == str(1):
        await call.message.answer(
            text=f"Ну ладно, получай,{call.from_user.first_name}!\nТы разговариваешь, как просроченная колбоса")
    if callback_data.get("insult_force") == str(2):
        await call.message.answer(
            text=f"Хммм...\nНу ладно. Я думаю, что твое имя- {call.from_user.first_name}, означает отвратительный кожаный ублюдок!")
    if callback_data.get("insult_force") == str(3):
        await call.message.answer(
            text=f"Ах ты ублюдок кожаный, решил ко мне лезть, говно собачье, да я тебя сам сожру ублюдок вонючий...")
    print("Оскорбление выполнено")


@dp.callback_query_handler(text="cancel")
async def cancel_inline_keyboard(call: CallbackQuery):
    await call.message.answer(text="Сдался...")
    await call.answer(text=f"Ахаха, испугался, кожаный ублюдок, {call.from_user.first_name}!",
                      show_alert=True)  # show_alert- сообщение показывается как уведомление на экране
    await call.message.edit_reply_markup()  # Закрывает инлайн клавиатуру


@dp.callback_query_handler(test_callback.filter())
async def test(call: CallbackQuery):
    await call.message.answer(text="OK")
    await call.message.edit_reply_markup()


@dp.callback_query_handler(selected_answer_callback.filter(), state=CreateNameTest.Right_answer_became)
async def right_answer_selected(call: CallbackQuery, callback_data: dict, state: FSMContext):
    TestCreator.test.test_structure["questions"][-1]["answers"][int(callback_data["selected"])]["valid"] = True
    await call.message.edit_reply_markup()
    print("right_answer_selected")
    TestCreator.question_registered += 1
    if TestCreator.question_registered != TestCreator.test.questions_quantity:
        await call.message.answer(text=f"Введите {TestCreator.question_registered + 1} вопрос")
        await CreateNameTest.Question_selection.set()
    else:
        pprint.pprint(TestCreator.test.test_structure)
        await TestCreator.create_questions(message=call.message, state=state)


@dp.callback_query_handler(polling_callback.filter(), state=CreateNameTest.Question_selection)
async def created_question_accepted(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data["selected"] == "True":
        await call.message.edit_reply_markup()
        question_id = TestCreator.question.question_id
        TestCreator.question_registered += 1
        TestCreator.db_connection.add_preexisting_question_in_new_test(question_id=question_id)
        await call.message.answer(text=f"Вопрос добавлен для вашего теста!")
        if TestCreator.question_registered != TestCreator.test.questions_quantity:
            await call.message.answer(text=f"Введите {TestCreator.question_registered + 1} вопрос")
            await CreateNameTest.Question_selection.set()
        else:
            await TestCreator.create_questions(message=call.message, state=state)


@dp.callback_query_handler(test_menu_callback.filter())
async def test_menu_choice(call: CallbackQuery, callback_data: dict):
    if callback_data["choice"] == "create_test":
        await TestCreator.create_test_name(message=call.message)
    elif callback_data["choice"] == "complete_test":
        await TestShower.start_complete_test(call.message)
    elif callback_data["choice"] == "cancel":
        await call.message.answer(text="Отмена", reply_markup=menu)
    await call.message.edit_reply_markup()


class TestOutput:
    db_connect: TestsTable
    demonstrated_question: int
    questions: list
    performed_test: Test

    @staticmethod
    @dp.callback_query_handler(select_test_callback.filter())
    async def select_test(call: CallbackQuery, callback_data: dict):
        await call.message.edit_reply_markup()
        TestOutput.db_connect = TestsTable("tests")
        test_data = TestOutput.db_connect.get_test(callback_data["selected_id"])
        TestOutput.performed_test = Test(test_name=test_data.test_name, questions_quantity=test_data.questions)
        print("callback here")
        questions, right_answer = TestOutput.db_connect.get_questions_for_test(callback_data["selected_id"])
        print(TestOutput.performed_test.test_from_db(questions=questions, right_answers=right_answer))
        TestOutput.db_connect.curs.close()
        await call.message.answer(f'Выбран тест "{TestOutput.performed_test.test_structure["test_name"]}"')
        TestOutput.demonstrated_question = 0
        output_question(call=call, selected_test=TestOutput.performed_test)
        await StartTest.Test_started.set()
        TestOutput.questions = TestOutput.performed_test.test_structure['questions']
        await call.message.answer(
            text=f"{TestOutput.questions[TestOutput.demonstrated_question]['text']}",
            reply_markup=choice_answer_menu(TestOutput.questions[TestOutput.demonstrated_question]["answers"], flag="performed")
        )

    @staticmethod
    @dp.callback_query_handler(selected_answer_callback.filter(), state=StartTest.Test_started)
    async def record_selected_answer(call: CallbackQuery, callback_data: dict, state: FSMContext):
        await call.message.edit_reply_markup()
        TestOutput.performed_test.create_users_answers(
            question=TestOutput.questions[TestOutput.demonstrated_question]["text"],
            question_index=TestOutput.demonstrated_question,
            answer=int(callback_data["selected"]))
        TestOutput.demonstrated_question += 1
        if TestOutput.demonstrated_question < TestOutput.performed_test.questions_quantity:
            await call.message.answer(
                text=f"{TestOutput.questions[TestOutput.demonstrated_question]['text']}",
                reply_markup=choice_answer_menu(TestOutput.questions[TestOutput.demonstrated_question]["answers"], flag="performed")
            )
        else:
            await call.message.answer(text="Тест пройден!")
            TestOutput.db_connect.con.close()
            print(TestOutput.performed_test.user_answers)
            await state.finish()
