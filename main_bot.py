from preference import TOKEN
from aiogram import Bot, Dispatcher, types, executor
import asyncio
import logging

bot = Bot(token=TOKEN)

dp = Dispatcher(bot=bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def hello(message: types.Message):
    await message.answer("Hi, I am Bot for creating picture composed of number")

executor.start_polling(dp, skip_updates=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



