from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
import os


load_dotenv()

bot = Bot(os.getenv('TOKEN_API'))
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("/help")
b2 = KeyboardButton("/description")
b3 = KeyboardButton("/image")
b4 = KeyboardButton("/location")
b5 = KeyboardButton("❤️")
kb.add(b1).add(b2).add(b3).add(b4).add(b5)

TEXT_HELP = '''/help - Отримати інформацію про команди
/image - Отримати картинку
/location - Отримати локацію
/start - Почати роботу з ботом
/desription - Отримати опис бота'''


@dp.message_handler(commands=["start"])
async def get_start(message: types.Message):
    await message.answer(text="Ласкавимо просимо у бот!",
                         reply_markup=kb)

@dp.message_handler(commands=["description"])
async def get_descr(message: types.Message):
    await message.answer(text='Цей бот використовується для вивчання модуля aiogram'
                         )
    await message.delete()


@dp.message_handler(commands=["help"])
async def get_help(message: types.Message):
    await message.answer(text=TEXT_HELP)
    await message.delete()

@dp.message_handler(commands=["image"])
async def get_image(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="https://w.forfun.com/fetch/32/3206bb3089350c851170b2c5ac00a6e8.jpeg"
                         )
    await message.delete()

@dp.message_handler(commands=["location"])
async def get_location(message: types.Message):
    await bot.send_location(chat_id=message.from_user.id,
                            latitude=53,
                            longitude=21
                            )
    await message.delete()

@dp.message_handler()
async def get_heart(message: types.Message):
    if message.text == "❤️":
        await bot.send_sticker(message.from_user.id,
                               sticker="CAACAgIAAxkBAAEJhSpknG5EJ3clblZU02f6nrd2IlUlaQAC6RUAApiqmEgcx3kHpFw_QS8E"
                               )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)