from preference import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.message import ContentType
from aiogram.types.bot_command import BotCommand

import bot_image
import logging
import asyncio







async def main():
    bot = Bot(token=TOKEN)

    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    logging.basicConfig(level=logging.INFO)

#States for automat 
    class State_for_image(StatesGroup):
        
        waiting_image = State()
        waiting_parametrs = State()
        waiting_set_parametr_1 = State()
        waiting_set_parametr_1 = State()
    
    class State_for_blur(StatesGroup):

        blur_number = State()
#Simple command
    @dp.message_handler(commands="start")
    async def hello(message: types.Message):
        await message.answer("Hi, I am Bot for creating picture composed of number/ Привет я бот который создает из фото картины по номерам")

    @dp.message_handler(commands='about')
    async def about(message: types.Message):
        await message.reply("I am Bot. My code in GitHub: github.com/Vetka20/Telegram_Bot")

    
    @dp.message_handler(commands="cancel", state = "*")
    @dp.message_handler(regexp="отмена",state="*")
    @dp.message_handler(regexp="Cancel",state="*")
    async def cancel(message: types.Message, state: FSMContext):
        await message.answer("Cancel")
        await state.finish()
    
    @dp.message_handler(commands="remake")
    async def remake_result_image(message: types.Message, state: FSMContext):
        await message.answer("I start create result image and countour, please wait")
        bot_image.correct(id=message.from_id ,src_image=f"/home/vetka/Telegram_Bot/images/{message.from_id}/buffer.jpg")
        await message.answer("I finish remake image. Now use comamnd /get_image")

    @dp.message_handler(commands="get_image")
    async def send_result_image(message: types.Message, state: FSMContext):
        photo = open(f"/home/vetka/Telegram_Bot/images/{message.from_id}/result.jpg", 'rb')
        await bot.send_photo(chat_id=message.from_id, photo=photo)

    @dp.message_handler(commands="get_countur")
    async def send_result_image(message: types.Message, state: FSMContext):
        photo = open(f"/home/vetka/Telegram_Bot/images/{message.from_id}/result_countur.jpg", 'rb')
        await bot.send_photo(chat_id=message.from_id, photo=photo)
    
    @dp.message_handler(commands="save")
    async def save_result(message: types.Message):
        await message.answer("Start save")
        bot_image.save(dst_from=f"/home/vetka/Telegram_Bot/images/{message.from_id}/result.jpg", dst_to=f"/home/vetka/Telegram_Bot/images/{message.from_id}/buffer.jpg")
        await message.answer("Done")

    @dp.message_handler(commands="restart_image")
    async def save_result(message: types.Message):
        await message.answer("Chose original image")
        bot_image.save(dst_from=f"/home/vetka/Telegram_Bot/images/{message.from_id}/image.jpg", dst_to=f"/home/vetka/Telegram_Bot/images/{message.from_id}/buffer.jpg")
        await message.answer("Done")

    @dp.message_handler(commands="histogram")
    async def histogram(message: types.Message):
        await message.answer("Hist")
        bot_image.full_diagram(dst=f"/home/vetka/Telegram_Bot/images/{message.from_id}/buffer.jpg", color = [0,32,64,96,128,160,192,224,255])

#FSM command
    @dp.message_handler(commands='blur')
    async def blur(message: types.Message, state: FSMContext):
        await message.answer("It is use normal blur")
        await state.set_state(State_for_blur.blur_number)
        
        await message.answer("Write the number(N), for filter 2D with matrix NxN")

    @dp.message_handler(regexp=r'[0-9]',state=State_for_blur.blur_number)
    async def blur_matrix(message: types.Message, state: FSMContext):
        N = int(message.text)
        N_vector = []
        N_matrix = []
        await message.answer(f"I start blur image with {N}x{N} matrix")
        for i in range(0,N):
            N_vector.append(1)
        for i in range(0,N):
            N_matrix.append(N_vector)
        bot_image.filter_levels(filter_matrix=N_matrix,levels={0:1,1:1,2:1}, dst=f"images/{message.from_user.id}")
        await state.finish()
        await message.answer("Done")
    




   

        

    @dp.message_handler(commands="create_image", state="*")
    async def image_start(message: types.Message, state: FSMContext):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add("Upload image")
        keyboard.add("Custom color")
        
        keyboard.add("Cancel")
        await message.answer("Chose what step you want?", reply_markup=keyboard)
        await state.set_state(State_for_image.waiting_parametrs)

    @dp.message_handler(state=State_for_image.waiting_set_parametr_1)
    async def set_parametr_1(message: types.Message, state: FSMContext):
        
        if message.text.lower == "all":
            message.answer("Done")
            state.set_state(State_for_image.waiting_parametrs)
        

    @dp.message_handler(state=State_for_image.waiting_parametrs)
    async def set_parametrs_image(message: types.Message, state: FSMContext):
        match message.text.lower():
            case "upload image":
                await message.answer("Wait your Photo")
                await state.set_state(State_for_image.waiting_image)
            case "custom color":
                await message.answer("Change color palitr")
                await state.set_state(State_for_image.waiting_set_parametr_1)
            
            case _:
                await message.answer("You didn`t choise the button, please push the button or send 'cancel'")
                return
            
        

    @dp.message_handler(content_types=ContentType.PHOTO,state=State_for_image.waiting_image)
    async def upload_image(message: types.Message, state: FSMContext):
        await message.photo[-1].download(destination=f"images/{message.from_id}/image.jpg")
        await message.photo[-1].download(destination=f"images/{message.from_id}/buffer.jpg")
        await message.answer("You send Photo. I download images for you, but you send photo. If you want more resolution, send photo as document. If you have small resolution or finish send ''.")

    @dp.message_handler(content_types=ContentType.DOCUMENT,state=State_for_image.waiting_image)
    async def upload_image(message: types.Message, state: FSMContext):
        await message.document.download(destination=f"images/{message.from_id}/image.jpg")
        await message.document.download(destination=f"images/{message.from_id}/buffer.jpg")
        await message.answer("I get photo in full resolution")
        
    
    
    await set_commands(bot=bot)
    await dp.skip_updates()
    await dp.start_polling()
    #executor.start_polling(dp, skip_updates=True)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='create_image', description='For upload image'),
        BotCommand(command='remake', description='For remake image to result'),
        BotCommand(command='get_image', description='For get final image'),
        BotCommand(command='get_countur', description='For get final countur of image'),
        BotCommand(command='blur', description='For image'),
        BotCommand(command='save', description='For save image'),
        BotCommand(command='restart_image', description='For chose original image'),
        BotCommand(command='cancel', description='For cancel FSM'),
    ]
    await bot.set_my_commands(commands=commands)

    



if __name__ == "__main__":
    asyncio.run(main())



