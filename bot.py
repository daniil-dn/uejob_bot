import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

import token
from sqllighter3 import SQLighter

from stopgameParser import StopGame

logging.basicConfig(level=logging.INFO)

# Bot init
bot = Bot(token=token.TOKEN)
dp = Dispatcher(bot)
db = SQLighter('db.db')

# Parser init
sg = StopGame('lastkey.txt')


@dp.message_handler(commands=['subscribe'])
async def sub(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # if user is not in the database, add him to the database
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)
    await message.answer("Вы подписаны на нашу рассылку!")


@dp.message_handler(commands=['unsubscribe'])
async def unsub(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # if user is not in the database, add him to the database
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы  итак не подписаны.")
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны.")


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        new_games = sg.new_games()

        if new_games:
            new_games.reverse()
            for ng in new_games:
                nfo = sg.game_info(ng)

                subscriptions = db.get_subsctioptions()
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                            s[1], photo, caption=nfo['title'] + 'Rating: ' + '\n' +
                                                 nfo['excerpt'] + "\n\n" + nfo['link'], disable_notification=True

                        )
                sg.update_lastkey(nfo['id'])


if __name__ == "__main__":
    # asyncio.get_event_loop().create_task(scheduled(1))
    executor.start_polling(dp, skip_updates=True)
