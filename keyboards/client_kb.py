from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('/sсhedule')
b2 = KeyboardButton('/place')
b3 = KeyboardButton('/menu')
b4 = KeyboardButton('/load')
# b4 = KeyboardButton('Share number', request_contact=True)
# b5 = KeyboardButton('Share location', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# kb_client.add(b1).add(b2).insert(b3)
kb_client.row(b1, b2, b3)
kb_client.row(b4)
