import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from testing.sqllighter3 import SQLighter

logging.basicConfig(level=logging.INFO)

# Bot init
bot = Bot(token="5104338493:AAGQ5mlJMGDlgRiSWdEDt3A7nkYHRAZz3As")
dp = Dispatcher(bot)
db = SQLighter('../db.db')

@dp.message_handler(commands=['start'])
async def sub(message: types.Message):
    await bot.send_message(message.chat.id, text=f"Hello, {message.from_user.full_name}")


if __name__ == "__main__":
    # asyncio.get_event_loop().create_task(scheduled(1))
    executor.start_polling(dp, skip_updates=True)
