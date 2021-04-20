import logging
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_shutdown(dp):
    await bot.close
    await storage.close()


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp)
