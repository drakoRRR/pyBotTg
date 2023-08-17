from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("/help")
b2 = KeyboardButton("/description")
b3 = KeyboardButton("/image")
b4 = KeyboardButton("/location")
b5 = KeyboardButton("❤️")
b6 = KeyboardButton("/download_vid")
kb.insert(b1).insert(b2).insert(b3).insert(b4).insert(b5).insert(b6)