import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

import mytoken
from sqllighter3 import SQLighter

from stopgameParser import StopGame

logging.basicConfig(level=logging.INFO)

# Bot init
bot = Bot(token=mytoken.TOKEN)
dp = Dispatcher(bot)
db = SQLighter('db.db')

# Parser init
sg = StopGame('lastkey.txt')

# @dp.message_handler(commands=['subscribe'])
@dp.message_handler(content_types=['text'])
async def sub(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    # asyncio.get_event_loop().create_task(scheduled(1))
    executor.start_polling(dp, skip_updates=True)
