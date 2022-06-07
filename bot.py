import logging

from aiogram import Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.utils.executor import start_webhook

from configs.mytoken import TOKEN as API_TOKEN
from Vacancy import vacancy_per_user, Vacancy, types
from configs.markup_text import help_text, AFTER_SEND_MP, AFTER_SEND_ALERT
from configs.config import WEBHOOK_HOST, WEBAPP_HOST, WEBAPP_PORT, WHERE_SEND

# from testing.sqllighter3 import SQLighter
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


def chat_message_id(message: types.Message) -> tuple:
    """

    :param message:
    :return: chat_id and message_id
    """
    match type(message):
        case types.Message:
            return message.chat.id, message.message_id
        case types.CallbackQuery:
            return message.message.chat.id, message.message.message_id


# очищает историю сообщений, по default - 2 последних
async def delete_prev_messages(current_message_id, chat_id, count_to_delete=2):
    if not (chat_id and current_message_id):
        return
    counter = current_message_id
    while True:
        if counter == current_message_id - count_to_delete:
            break
        try:
            await bot.delete_message(chat_id=chat_id, message_id=counter)
        except Exception as err:
            print('No message to dlt')
            continue
        finally:
            counter -= 1


# очищает клавиатуру сообщений, по default - 2 последних включительно текущее
async def clear_markup(current_message_id, chat_id, count_to_delete=5):
    """# очищает markup, по default - 2— последних"""
    if not (chat_id and current_message_id):
        return
    counter = current_message_id
    while True:
        if counter == current_message_id - count_to_delete:
            break
        try:
            await bot.edit_message_reply_markup(chat_id=chat_id, message_id=counter, reply_markup=None)
        except:
            print('No message to clear')
            continue
        finally:
            counter -= 1


# Команда для полной перезагрузки и начала с меню
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    pass

@dp.message_handler(commands=['new'])
@dp.callback_query_handler(lambda call: call.data.startswith('/new'))
async def new_vacancy(message: types.Message):
    pass


# Работа с данными без клавиатуры - описание, и др., где требуется ввод с клавиатуры
@dp.message_handler()
async def text_handler(message: types.Message):
    pass


# Меню заполнения вакансии
@dp.callback_query_handler(lambda call: call.data == 'back_menu')
async def menu_return(cb):
    pass


@dp.callback_query_handler(lambda call: call.data.startswith('clear_'))
async def clear_field(cb):
    pass


@dp.callback_query_handler(lambda call: call.data in ('Intern', 'Junior', 'Middle', "Senior"))
async def jun_mid_sen(cb):
    pass


@dp.callback_query_handler(
    lambda call: call.data in ('Remote', 'PC', "Console", "VR/AR", "Mobile", 'Relocate'))
async def platform_cb(cb):
    pass


@dp.callback_query_handler(
    lambda call: call.data in ('Full-Time', "Part-Time", "Contract"))
async def schedule(cb):
    pass


@dp.callback_query_handler(
    lambda call: call.data in ("send_verif"))
async def send_verif(cb):
    pass


@dp.callback_query_handler(
    lambda call: call.data in ("reset_verif"))
async def reset_verif(cb):
    pass


@dp.callback_query_handler(
    lambda call: call.data in ("Negotiable"))
async def pay(cb):
    pass


# Меню заполнения вакансии
# проверка cb на тег меню
@dp.callback_query_handler(lambda call: True)
async def callback4_all(cb):
    pass


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
