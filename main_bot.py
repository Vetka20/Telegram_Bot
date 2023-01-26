from preference import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.message import ContentType

import bot_image
import asyncio
import logging

bot = Bot(token=TOKEN)

dp = Dispatcher(bot=bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands="start")
async def hello(message: types.Message):
    await message.answer("Hi, I am Bot for creating picture composed of number/ Привет я бот который создает из фото картины по номерам")

@dp.message_handler(commands='about')
async def about(message: types.Message):
    await message.reply("I am Bot. My code in GitHub: github.com/Vetka20/Telegram_Bot")

#States for automat 
class State_for_image(StatesGroup):
    
    waiting_image = State()
    waiting_parametrs = State()

@dp.message_handler(commands="create_image", state="*")
async def image_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Upload image")
    
    keyboard.add("Cancel")
    await message.answer("Chose what step you want?", reply_markup=keyboard)
    await state.set_state(State_for_image.waiting_parametrs)

@dp.message_handler(state=State_for_image.waiting_parametrs)
async def set_parametrs_image(message: types.Message, state: FSMContext):
    if message.text.lower()!="upload image":
        await message.answer("You didn`t choise the button, please push the button or send 'cancel'")
        return
    await message.answer("Wait your Photo")
    await state.set_state(State_for_image.waiting_image)

@dp.message_handler(content_types=ContentType.PHOTO,state=State_for_image.waiting_image)
async def upload_image(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination=f"images/{message.from_id}/image.jpg")
    await message.answer("You send Photo. I download images for you, but you send photo. If you want more resolution, send photo as document. If you have small resolution or finish send ''.")

@dp.message_handler(content_types=ContentType.DOCUMENT,state=State_for_image.waiting_image)
async def upload_image(message: types.Message, state: FSMContext):
    await message.document.download(destination=f"images/{message.from_id}/image.jpg")
    await message.answer("I get photo in full resolution")
    
@dp.message_handler(commands="remake", state='*')
async def remake_result_image(message: types.Message, state: FSMContext):
    bot_image.correct(id=message.from_id ,src_image=f"/home/vetka/Telegram_Bot/images/{message.from_id}/image.jpg")
    await message.answer("I start create result image and countour, please wait")

@dp.message_handler(commands="get_image", state="*")
async def send_result_image(message: types.Message, state: FSMContext):
    photo = open(f"/home/vetka/Telegram_Bot/images/{message.from_id}/result.jpg", 'rb')
    await bot.send_photo(chat_id=message.from_id, photo=photo)
    

@dp.message_handler(commands="cancel", state = "*")
@dp.message_handler(regexp="отмена",state="*")
@dp.message_handler(regexp="Cancel",state="*")
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Cancel")
    await state.finish()
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



