import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from mytoken import TOKEN as API_TOKEN
from Vacancy import vacancy_per_user, Vacancy, types
from testing.sqllighter3 import SQLighter

WEBHOOK_HOST = 'https://a3b6-185-135-150-187.ngrok.io'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 80

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# очищает историю сообщений, по default - 5 последних
async def clear_prev_messages(current_message, chat_id, count_to_delete=5):
    if not (chat_id and current_message):
        return None
    counter = current_message
    while True:
        counter -= 1
        if counter == current_message - count_to_delete:
            break
        try:
            await bot.delete_message(chat_id=chat_id, message_id=counter)
        except:
            print('No message to dlt')
            continue


# Команды для старта или создания новой вакансии
@dp.message_handler(commands=['new', 'start'])
async def start_over(message: types.Message):
    # удаляет 5 последних сообщений
    await clear_prev_messages(message.message_id, chat_id=message.chat.id)

    # start message удаляется после первого callback
    start_message = await bot.send_message(message.chat.id, "🚀🚀🚀🚀🚀🚀🚀🚀🚀", reply_markup=None)
    mg = await bot.send_message(message.chat.id, "STARTING", reply_markup=None)

    cur_vacancy = Vacancy(message_id=mg.message_id, chat_id=message.chat.id)

    cur_vacancy.start_message = start_message
    # Вообще next_step вызывает внутри update_data, но можно и отдельно
    vacancy_per_user[message.chat.id] = cur_vacancy.next_step()

    kb = cur_vacancy.cur_kb
    text_message = cur_vacancy.cur_text_for_message
    await bot.edit_message_text(chat_id=cur_vacancy.chat_id, message_id=cur_vacancy.message_id, text=text_message,
                                reply_markup=kb)


@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message):
    chat_id = message.chat.id
    if not vacancy_per_user.get(chat_id, None):
        await start_over(message)


@dp.callback_query_handler(lambda call: True)
async def callback_inline(cb):
    chat_id = cb.message.chat.id
    cur_vacancy = vacancy_per_user.get(chat_id, None)

    # Если нет у текущего чата объекта вакансии - создает новый объект и присваивает к текущему чату,
    #   может произойти после ребута
    if not cur_vacancy:
        await bot.edit_message_text(chat_id=chat_id, message_id=cb.message.message_id, text="/start", reply_markup=None)
        await start_over(cb.message)
        return

    # Удаление первого сообщения с ракетами
    if cur_vacancy.start_message:
        await bot.delete_message(chat_id=cb.message.chat.id, message_id=cur_vacancy.start_message.message_id)
        cur_vacancy.start_message = None

    #  Логика внутри update_data
    #       Внутри update data будут происходить все действия - обновляет текущий шаг self.step += 1
    #       также update обновляет текущую клавиатуру и текст
    print(cur_vacancy.step, cur_vacancy.STAGES)
    cur_vacancy.update_data(cb.data)
    kb = cur_vacancy.cur_kb
    text_message = cur_vacancy.cur_text_for_message

    await bot.edit_message_text(chat_id=chat_id, message_id=cur_vacancy.message_id, text=text_message, reply_markup=kb)

    await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text=cb.data)


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
