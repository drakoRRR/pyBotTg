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
    WAITING_FOR_QUALITY = State()
    WAITING_FOR_MUSIC_TEXT = State()


@dp.message_handler(lambda message: message.text == "/start")
async def get_start(message: types.Message):
    return await message.answer(text=START_TEXT,
                                reply_markup=kb_main)

@dp.message_handler(lambda message: message.text == "📜 Опис Боту")
async def get_descr(message: types.Message):
    await message.answer(text=DESCRIPTION_TEXT)


@dp.message_handler(lambda message: message.text == "📝 Інструкція")
async def get_help(message: types.Message):
    await message.answer(text=TEXT_HELP)

@dp.message_handler(lambda message: message.text == "🎼 Завантажити пісню")
async def get_audio(message: types.Message):
    await Form.WAITING_FOR_MUSIC_TEXT.set()
    await message.answer("📍 Надішліть посилання на YouTube відео з аудіо якe хочете завантажити",
                         reply_markup=close_kb)


@dp.message_handler(lambda message: message.text.startswith("http"), state=Form.WAITING_FOR_MUSIC_TEXT)
async def process_text_audio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url_music'] = message.text

        url_youtube_music = data['url_music']

        try:
            video = YouTube(url_youtube_music)
            audio_stream = video.streams.filter(only_audio=True, file_extension="mp4").first()

            # Download the audio stream into a memory buffer
            buffer = BytesIO()
            audio_stream.stream_to_buffer(buffer)

            start_message = await message.answer("⚒ Йде завантаження аудіо...")

            buffer.seek(0)
            # Send the audio as a document to the user
            caption = video.title
            await bot.send_audio(message.chat.id,
                                 audio=types.InputFile(buffer, filename=video.title + ".mp3"),
                                 caption=caption,
                                 reply_markup=kb_main,
                                 )

            await state.finish()
            await bot.delete_message(message.chat.id, start_message.message_id)

        except Exception as e:
            await message.reply(f"❌ Помилка завантаження: {e} ❌", reply_markup=kb_main)

@dp.message_handler(lambda message: message.text == "🎥 Завантажити відео")
async def start_download(message: types.Message):
    await Form.WAITING_FOR_TEXT.set()
    await message.answer("📍 Надішліть посилання на відео яке хочете завантажити"
                         "(Не більше 5 хв, або більше, але максимальна якість буде 360р)", reply_markup=close_kb)


@dp.message_handler(lambda message: message.text.startswith("http"), state=Form.WAITING_FOR_TEXT)
async def process_text_video(message: types.Message, state: FSMContext):
    await Form.WAITING_FOR_QUALITY.set()  # Устанавливаем состояние ожидания выбора качества

    async with state.proxy() as data:
        data['url_video'] = message.text

    await message.answer(text='📍 Оберіть якість відео яке хочете завантажити:', reply_markup=kb_resolution)


@dp.message_handler(lambda message: message.text in ["360p", "720p", "1080p", "The best res"], state=Form.WAITING_FOR_QUALITY)
async def process_quality_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        url_youtube = data['url_video']
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
            video_title = video.title

            buffer.seek(0)  # Сбрасываем позицию буфера в начало
            await bot.send_video(message.chat.id,
                                 buffer,
                                 caption="Caption: " + video_title + " \nVideo Quality: " + user_choice)

            await bot.delete_message(message.chat.id, start_message.message_id)

            await state.finish()
            await message.reply("✅ Ваше відео у вибраній якості завантажено", reply_markup=kb_main)
        except Exception as e:
            await message.reply(f"❌ Помилка завантаження: {e} ❌", reply_markup=kb_main)
            await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)