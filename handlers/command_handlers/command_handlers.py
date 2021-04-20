# Обработчики

from main import bot, dp
from handlers.text_handlers.text_handlers import welcome_message
from keyboards.default import menu
from aiogram.types import Message
from config import admin_id
from aiogram.dispatcher.filters import Command


async def send_to_admin():
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler(Command("start"))
async def welcome(message: Message):
    await welcome_message(message)


@dp.message_handler(Command("menu"))
async def call_menu(message: Message):
    await message.answer("Чего надо?", reply_markup=menu)


@dp.message_handler(Command("creat_test"))
async def creat_test(message: Message):
    await message.reply(text="Напиши название теста")








