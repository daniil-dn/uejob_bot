import logging
import asyncio
from datetime import datetime
from collections import OrderedDict
from aiogram import Bot, Dispatcher, executor

import mytoken
from Vacancy import vacancy_per_user, Vacancy, types
from sqllighter3 import SQLighter
from stopgameParser import StopGame

logging.basicConfig(level=logging.INFO)

# Bot init
bot = Bot(token=mytoken.TOKEN)
dp = Dispatcher(bot)
db = SQLighter('db.db')


# @dp.message_handler(commands=['subscribe'])
@dp.message_handler(commands=['new'])
async def start_over(message: types.Message):
    vacancy_per_user[message.chat.id] = Vacancy()
    text = vacancy_per_user[message.chat.id].get_text()
    markup = vacancy_per_user[message.chat.id].get_markup()
    await bot.send_message(message.chat.id, "🚀 Starting", reply_markup=None)
    await bot.send_message(message.chat.id, text, reply_markup=markup)


@dp.message_handler(commands=['current'])
async def show_current_stage(message: types.Message):
    await bot.send_message(message.chat.id, str(f'You are at: '))


@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message):
    vacancy_per_user.setdefault(message.chat.id, Vacancy())
    vacancy_obj = vacancy_per_user[message.chat.id]
    if vacancy_obj.stage < len(vacancy_obj.STAGES):
        vacancy_obj.info[Vacancy.STAGES[vacancy_obj.stage]] = message.text.strip().lower()

        vacancy_obj.stage += 1
        if vacancy_obj.stage < len(vacancy_obj.STAGES):
            await bot.send_message(message.chat.id, vacancy_obj.get_text(), reply_markup=vacancy_obj.get_markup())

    if vacancy_obj.stage == len(vacancy_obj.STAGES):
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('/new'))
        await bot.send_message(message.chat.id, vacancy_obj.get_ready_vacancy(),
                               reply_markup=markup, parse_mode='html')


if __name__ == "__main__":
    # asyncio.get_event_loop().create_task(scheduled(1))
    executor.start_polling(dp, skip_updates=True)
