from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command, Text

from keyboards.inline_keyboards.callback_datas import test_callback
from states.test_10q.test_10q import TestTen

from keyboards.inline_keyboards.test_10q_choices import creat_keyboard

from main import dp, bot


@dp.message_handler(Command("test"), state=None)  # state None означает попадание в хэндлер без какого-либо состояния
async def start_test(message: Message):
    await message.answer(text="Вы начали тестирование")
    await message.answer(text="Вопрос №1\nКакой праздник празднуется в РФ 12 апреля?", reply_markup=creat_keyboard(["One", "Two", "Tree", "Four"]))
    await TestTen.first()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q1)
async def save_q1(answer: CallbackQuery, state: FSMContext):
    answer1 = str(answer["data"])
    await state.update_data(answer1=answer1)
    await bot.send_message(answer.from_user.id, text="Вопрос №2\nКто был первым императором Римской Империи?", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q2)
async def save_q2(answer: CallbackQuery, state: FSMContext):
    answer2 = str(answer["data"])
    await state.update_data(answer2=answer2)
    await bot.send_message(answer.from_user.id, text="Вопрос №3\nСколько букв в русском алфавите?", reply_markup=creat_keyboard(["First3", "Second3", "Third3", "Fourty3"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q3)
async def save_q3(answer: CallbackQuery, state: FSMContext):
    answer3 = str(answer["data"])
    await state.update_data(answer3=answer3)
    await bot.send_message(answer.from_user.id, text="Вопрос№4\nСтолица Словакии?", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q4)
async def save_q4(answer: CallbackQuery, state: FSMContext):
    answer4 = str(answer["data"])
    await state.update_data(answer4=answer4)
    await bot.send_message(answer.from_user.id, text="Вопрос№5\nКак звали коня Александра Македонского?", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q5)
async def save_q5(answer: CallbackQuery, state: FSMContext):
    answer5 = str(answer["data"])
    await state.update_data(answer5=answer5)
    await bot.send_message(answer.from_user.id, text="Вопрос№6\nСколько зубов у взрослого человека?", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q6)
async def save_q6(answer: CallbackQuery, state: FSMContext):
    answer6 = str(answer["data"])
    await state.update_data(answer6=answer6)
    await bot.send_message(answer.from_user.id, text="Вопрос№7\nСколько рёбер у человека?", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q7)
async def save_q7(answer: CallbackQuery, state: FSMContext):
    answer7 = str(answer["data"])
    await state.update_data(answer3=answer7)
    await bot.send_message(answer.from_user.id, text="Вопрос№8\nКакой самый распространенный язык в мире?", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q8)
async def save_q8(answer: CallbackQuery, state: FSMContext):
    answer8 = str(answer["data"])
    await state.update_data(answer8=answer8)
    await bot.send_message(answer.from_user.id, text="Вопрос№9\nКакая самая сильная мышца человеческого тела", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q9)
async def save_q9(answer: CallbackQuery, state: FSMContext):
    answer9 = str(answer["data"])
    await state.update_data(answer9=answer9)
    await bot.send_message(answer.from_user.id, text="Вопрос№10\nСколько Океанов на планете Земля?", reply_markup=creat_keyboard(["First", "Second", "Third", "Fourty"]))
    await TestTen.next()


@dp.callback_query_handler(test_callback.filter(), state=TestTen.Q10)
async def save_q10(answer: CallbackQuery, state: FSMContext):
    answer10 = str(answer["data"])
    await state.update_data(answer10=answer10)
    data = await state.get_data()
    print(data)
    await bot.send_message(answer.from_user.id, "Тест окончен, вывести ваши ответы и результат?")
    await state.finish()
