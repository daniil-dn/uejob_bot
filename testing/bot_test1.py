# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import telebot
import config
from datetime import datetime
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker_welcome = open('../stickers/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker_welcome)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Random number:')
    item2 = types.KeyboardButton('How are you?')
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     'Hi, {0.first_name}. I\'m <b>{1.first_name}</b>'.format(message.from_user,
                                                                             bot.get_me()), parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.chat.type == 'private':
        if message.text == 'Random number:':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'How are you?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Good', callback_data='good')
            item2 = types.InlineKeyboardButton('Bad', callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, "I'm fine. How are you? ", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "I don't know what to reply. Please, try again")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == "good":
            bot.send_message(call.message.chat.id, "That's great!")
        elif call.data == "bad":
            bot.send_message(call.message.chat.id, "That's not so good(")

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="I'm fine.", reply_markup=None)
        bot.answer_callback_query(show_alert=False, callback_query_id=call.id, text="It's a test message...")
    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
