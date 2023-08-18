from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputFile


# Close Keyboard
close_kb = ReplyKeyboardRemove()

# Start Keyboard
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton("📝 Інструкція")
b2 = KeyboardButton("📜 Опис Боту")
b3 = KeyboardButton("🎼 Завантажити пісню")
b4 = KeyboardButton("🎥 Завантажити відео")
kb_main.insert(b1).insert(b2).add(b3).add(b4)


# Keyboard for choosing resolution when user downloading video from YouTube
kb_resolution = ReplyKeyboardMarkup(resize_keyboard=True)
b1_res = KeyboardButton("360p")
b2_res = KeyboardButton("720p")
b3_res = KeyboardButton("1080p")
b4_res = KeyboardButton("The best res")
kb_resolution.insert(b1_res).insert(b2_res).insert(b3_res).insert(b4_res)

