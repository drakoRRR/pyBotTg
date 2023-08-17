import os
from io import BytesIO
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from pytube import YouTube
from texts_for_replys import *
from buttons import *


load_dotenv()
storage = MemoryStorage()


bot = Bot(os.getenv('TOKEN_API'))
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    WAITING_FOR_TEXT = State()


@dp.message_handler(commands=["start"])
async def get_start(message: types.Message):
    await message.answer(text=START_TEXT,
                         reply_markup=kb)

@dp.message_handler(commands=["description"])
async def get_descr(message: types.Message):
    await message.answer(text=DESCRIPTION_TEXT)
    await message.delete()


@dp.message_handler(commands=["help"])
async def get_help(message: types.Message):
    await message.answer(text=TEXT_HELP)

@dp.message_handler(commands=["image"])
async def get_image(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://w.forfun.com/fetch/32/3206bb3089350c851170b2c5ac00a6e8.jpeg"
                         )
    await message.delete()


@dp.message_handler(commands=["download_vid"])
async def start_download(message: types.Message):
    await Form.WAITING_FOR_TEXT.set()  # Set the state to waiting for text input
    await message.answer("Надішліть посилання на відео яке хочете завантажити")


@dp.message_handler(state=Form.WAITING_FOR_TEXT)  # Handle the user's response in this state
async def process_text(message: types.Message, state: FSMContext):
    url_youtube = message.text

    try:
        video = YouTube(url_youtube)
        stream = video.streams.get_highest_resolution()
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)

        buffer.seek(0)  # Reset buffer position to the beginning
        await bot.send_video(message.chat.id, buffer)
        await state.finish()
        await message.reply("Ваше відео у найкращій якості !!!")
    except Exception as e:
        await message.reply(f"Помилка завантаження: {e}")
        await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)