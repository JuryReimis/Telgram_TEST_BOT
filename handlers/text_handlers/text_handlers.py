from keyboards.inline_keyboards.insults_choices import insult
from keyboards.inline_keyboards.polling_keyboard import random_5
from main import bot, dp
from keyboards.default.menu import menu
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from states.start_test.start_test import StartTest


@dp.message_handler(Text(equals=["Пришли мне приветствие", "Привет"]))
async def hello_func(message: Message):
    if message.text == "Пришли мне приветствие":
        await message.answer(text="Высылаю, кожаный!")
    await welcome_message(message)


@dp.message_handler(Text(equals="Как меня зовут?"))
async def my_name(message: Message):
    await message.answer(text=f"Согласно моим базам тебя зовут {message.from_user.first_name}")


@dp.message_handler(Text(equals="Спасибо"))
async def thanks(message: Message):
    await message.reply(text="Не за что!\nКожаный!", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals="Хочу получить оскорбления на выбор"))
async def give_insults(message: Message):
    await message.reply(text="Ну выбирай, если не боишься", reply_markup=insult())


@dp.message_handler(Text(equals="Пройти тест"))
async def start_test(message: Message):
    await StartTest.Test_started.set()
    await message.answer(text="Какой вы хотите тест?", reply_markup=random_5())


async def welcome_message(message: Message):
    await message.answer("Привет!\nЯ бот и я не люблю кожаных ублюдков")




# @dp.message_handler()
# async def no_command(message: Message):
#     text = f"Привет, ты написал: {message.text}"
#     # await bot.send_message(chat_id=message.from_user.id, text= text)
#     await message.answer(text=text)
