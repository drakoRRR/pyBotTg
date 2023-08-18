import os
import time
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
    WAITING_FOR_QUALITY = State()


@dp.message_handler(lambda message: message.text == "/start")
async def get_start(message: types.Message):
    await message.answer(text=START_TEXT,
                         reply_markup=kb_main)

@dp.message_handler(lambda message: message.text == "📜 Опис Боту")
async def get_descr(message: types.Message):
    await message.answer(text=DESCRIPTION_TEXT)


@dp.message_handler(lambda message: message.text == "📝 Існтрукція")
async def get_help(message: types.Message):
    await message.answer(text=TEXT_HELP)

@dp.message_handler(lambda message: message.text == "🎼 Завантажити пісню")
async def get_image(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://w.forfun.com/fetch/32/3206bb3089350c851170b2c5ac00a6e8.jpeg"
                         )


@dp.message_handler(lambda message: message.text == "🎥 Завантажити відео")
async def start_download(message: types.Message):
    await Form.WAITING_FOR_TEXT.set()
    await message.answer("Надішліть посилання на відео яке хочете завантажити", reply_markup=close_kb)


@dp.message_handler(lambda message: message.text.startswith("http"), state=Form.WAITING_FOR_TEXT)
async def process_text(message: types.Message, state: FSMContext):
    await Form.WAITING_FOR_QUALITY.set()  # Устанавливаем состояние ожидания выбора качества

    async with state.proxy() as data:
        data['url'] = message.text

    await message.answer(text='Оберіть якість відео яке хочете завантажити:', reply_markup=kb_resolution)


@dp.message_handler(lambda message: message.text in ["360p", "720p", "1080p", "The best res"], state=Form.WAITING_FOR_QUALITY)
async def process_quality_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        url_youtube = data['url']
        user_choice = message.text

        try:
            video = YouTube(url_youtube)
            if user_choice != "The best res":
                stream = video.streams.get_by_resolution(user_choice)
            else:
                stream = video.streams.get_highest_resolution()
            buffer = BytesIO()
            stream.stream_to_buffer(buffer)

            start_message = await message.answer("⚒ Йде завантаження відео...")

            buffer.seek(0)  # Сбрасываем позицию буфера в начало
            await bot.send_video(message.chat.id, buffer)

            await bot.delete_message(message.chat.id, start_message.message_id)

            await state.finish()
            await message.reply("✅ Ваше відео у вибраній якості завантажено", reply_markup=kb_main)
        except Exception as e:
            await message.reply(f"❌ Помилка завантаження: {e} ❌")
            await state.finish()



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)