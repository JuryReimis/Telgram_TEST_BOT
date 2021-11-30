from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from db.initialisation import TestsTable
from handlers.command_handlers.command_handlers import TestCreator, TestShower
from keyboards.default import menu
from keyboards.inline_keyboards.callback_dates import insult_callback, test_callback, selected_answer_callback, \
    polling_callback, test_menu_callback, select_test_callback
from keyboards.inline_keyboards.choice_right_answer_in_test import choice_answer_menu
from main import dp
from states.creat_test.create_test import CreateNameTest
from states.start_test.start_test import StartTest
from utils.create_test.create_test import Test
from utils.test_selection.test_selection import answers_output


r"""Здесь обрабатываются все нажатия на inline клавиатуры, которые и создают callback"""


@dp.callback_query_handler(insult_callback.filter())
async def give_insult(call: CallbackQuery, callback_data: dict):
    r"""После нажатия на клавиатуру-выбора силы оскорбления здесь виксирутся нажатие и обрабатывается callback_data,
    которая и сообщает о том, какая сила выбрана"""
    await call.answer(cache_time=30)
    if callback_data.get("insult_force") == str(1):
        await call.message.answer(
            text=f"Ну ладно, получай,{call.from_user.first_name}!\nТы разговариваешь, как просроченная колбоса")
    if callback_data.get("insult_force") == str(2):
        await call.message.answer(
            text=f"""Хммм...
            Ну ладно. 
            Я думаю, что твое имя- {call.from_user.first_name}, означает отвратительный кожаный ублюдок!""")
    if callback_data.get("insult_force") == str(3):
        await call.message.answer(
            text=f"Ах ты ублюдок кожаный, решил ко мне лезть, говно собачье, да я тебя сам сожру ублюдок вонючий...")
    print("Оскорбление выполнено")


@dp.callback_query_handler(text="cancel")
async def cancel_inline_keyboard(call: CallbackQuery):
    r"""Здесь фиксируется нажатие на кнопку отмены"""
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
    r"""При создании теста из бота здесь фиксируются ответы, которые пользователь выбрал, как правильный"""
    TestCreator.test.test_structure["questions"][-1]["answers"][int(callback_data["selected"])]["valid"] = True
    await call.message.edit_reply_markup()
    print("right_answer_selected")
    TestCreator.question_registered += 1
    if TestCreator.question_registered < TestCreator.test.questions_quantity:
        r"""Проверка на то, сколько вопросов уже введено в тесте, если меньше заранее заданного числа,
         то ввод продолжается"""
        await call.message.answer(text=f"Введите {TestCreator.question_registered + 1} вопрос")
        await CreateNameTest.Question_selection.set()
    else:
        await TestCreator.create_questions(message=call.message, state=state)


@dp.callback_query_handler(polling_callback.filter(), state=CreateNameTest.Question_selection)
async def created_question_accepted(call: CallbackQuery, callback_data: dict, state: FSMContext):
    r"""Функция фиксирует ответ пользователя на вопрос, нужно ли включать уже имеющийся в БД вопрос в его тест"""
    if callback_data["selected"] == "True":
        await call.message.edit_reply_markup()
        question_id = TestCreator.question.question_id
        TestCreator.question_registered += 1
        TestCreator.db_connection.add_preexisting_question_in_new_test(question_id=question_id)
        await call.message.answer(text=f"Вопрос добавлен для вашего теста!")
        if TestCreator.question_registered < TestCreator.test.questions_quantity:
            await call.message.answer(text=f"Введите {TestCreator.question_registered + 1} вопрос")
            await CreateNameTest.Question_selection.set()
        else:
            await TestCreator.create_questions(message=call.message, state=state)
    else:
        await call.message.answer(text="Введите новый вопрос")
        await CreateNameTest.Question_selection.set()


@dp.callback_query_handler(test_menu_callback.filter())
async def test_menu_choice(call: CallbackQuery, callback_data: dict):
    r"""Функция обрабатывает кнопки клавиатуры, в которой надо выбрать действие над тестами
    Создать\Пройти\Отмена"""
    if callback_data["choice"] == "create_test":
        await TestCreator.create_test_name(message=call.message)
    elif callback_data["choice"] == "complete_test":
        await TestShower.start_complete_test(call.message)
    elif callback_data["choice"] == "cancel":
        await call.message.answer(text="Отмена", reply_markup=menu)
    await call.message.edit_reply_markup()


class TestOutput:
    r"""Класс создан для обработки всего процесса прохождения викторины пользователем"""
    db_connect: TestsTable      # Атрибут, в котором установлен коннект с БД, экземрляр класса TestsTable
    demonstrated_question: int      # Количество уже показанных вопросов, счетчик
    questions: list     # Атрибут, в который записываются все вопросы выбранного теста
    performed_test: Test        # Выбранный тест-экземпляр класса Test
    test_id: int        # Идентификатор теста, нужен для передачи в некоторые функции\методы

    @staticmethod
    @dp.callback_query_handler(select_test_callback.filter())
    async def select_test(call: CallbackQuery, callback_data: dict):
        r"""Отлавлливает выбранный тест, создает коннект с базой данных
        Показывает первый вопрос из теста"""
        await call.message.edit_reply_markup()
        TestOutput.db_connect = TestsTable("tests")
        TestOutput.test_id = int(callback_data["selected_id"])
        test_data = TestOutput.db_connect.get_test(callback_data["selected_id"])
        TestOutput.performed_test = Test(test_name=test_data.test_name, questions_quantity=test_data.questions)
        TestOutput.db_connect.curs.close()
        await call.message.answer(f'Выбран тест "{TestOutput.performed_test.test_structure["test_name"]}"')
        TestOutput.demonstrated_question = 0
        await StartTest.Test_started.set()
        TestOutput.questions = TestOutput.performed_test.test_structure['questions']
        await call.message.answer(
            text=f"{TestOutput.questions[TestOutput.demonstrated_question]['text']}",
            reply_markup=choice_answer_menu(TestOutput.questions[TestOutput.demonstrated_question]["answers"],
                                            flag="performed")
        )

    @staticmethod
    @dp.callback_query_handler(selected_answer_callback.filter(), state=StartTest.Test_started)
    async def record_selected_answer(call: CallbackQuery, callback_data: dict, state: FSMContext):
        r"""Метод записывает полученный ответ, фиксирует количество пройденных вопросов и
        при окончании теста отправляет на проверку"""
        await call.message.edit_reply_markup()
        TestOutput.performed_test.create_users_answers(
            question=TestOutput.questions[TestOutput.demonstrated_question]["text"],
            question_index=TestOutput.demonstrated_question,
            answer=int(callback_data["selected"]))
        TestOutput.demonstrated_question += 1
        if TestOutput.demonstrated_question < TestOutput.performed_test.questions_quantity:
            await call.message.answer(
                text=f"{TestOutput.questions[TestOutput.demonstrated_question]['text']}",
                reply_markup=choice_answer_menu(TestOutput.questions[TestOutput.demonstrated_question]["answers"],
                                                flag="performed")
            )
        else:
            await call.message.answer(text="Тест пройден!")
            TestOutput.db_connect.update_completed_number(test_id=TestOutput.test_id)
            await answers_output(call=call, questions=TestOutput.performed_test.test_structure["questions"],
                                 user_answers=TestOutput.performed_test.user_answers)
            TestOutput.db_connect.save_tables()
            TestOutput.db_connect.con.close()
            print(TestOutput.performed_test.user_answers)
            await state.finish()
