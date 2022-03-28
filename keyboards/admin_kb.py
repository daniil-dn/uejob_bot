from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b1 = KeyboardButton('/load')
b2 = KeyboardButton('/delete')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# kb_client.add(b1).add(b2).insert(b3)
kb_admin.row(b1, b2)
