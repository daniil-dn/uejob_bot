import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from mytoken import TOKEN as API_TOKEN
from Vacancy import vacancy_per_user, Vacancy, types
from testing.sqllighter3 import SQLighter

WEBHOOK_HOST = 'https://2f1b-185-135-150-187.ngrok.io'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 4443

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
        if counter == current_message - count_to_delete:
            break
        try:
            await bot.delete_message(chat_id=chat_id, message_id=counter)

        except:
            print('No message to dlt')
            continue
        finally:
            counter -= 1


# Команды для старта или создания новой вакансии
@dp.message_handler(commands=['new', 'start'])
async def start_over(message: types.Message):
    # удаляет 5 последних сообщений, НО - 1 поэтому не удаляет текущее
    await clear_prev_messages(message.message_id - 1, chat_id=message.chat.id)

    # start_message удаляется после первого callback
    start_message = await bot.send_message(message.chat.id, "🚀🚀🚀🚀🚀🚀🚀🚀🚀", reply_markup=None)

    # Сообщение, с которым будем работать. И позже запихиваем его в объект вакансии
    mg = await bot.send_message(message.chat.id, "STARTING", reply_markup=None, parse_mode='html')
    # Инициализация объекта вакансии с главным сообщением и чатом
    cur_vacancy = Vacancy(message_id=mg.message_id, chat_id=message.chat.id)

    # Чтобы в первом callback удалить Start_message
    cur_vacancy.start_message = start_message

    # Привязываем вакансию к чату
    vacancy_per_user[message.chat.id] = cur_vacancy

    # При создании вакансии автоматически инициализируется клавиатура и текст
    kb, text_message = cur_vacancy.cur_kb, cur_vacancy.cur_text_for_message
    await bot.edit_message_text(chat_id=cur_vacancy.chat_id, message_id=cur_vacancy.message_id, text=text_message,
                                reply_markup=kb, parse_mode='html')


# TODO сделать меню = позже
@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    pass


# TODO Работа с данными без клавиатуры - описание, и др.
@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message):
    chat_id = message.chat.id
    cur_vacancy = vacancy_per_user.get(chat_id, None)
    if not cur_vacancy:
        await start_over(message)
    else:
        data = message.text
        cur_vacancy.update_data(data)
        cur_vacancy.next_step()

        kb = cur_vacancy.cur_kb
        text_message = cur_vacancy.cur_text_for_message

        # удаляет сообщение пользователя, когда не надо вводить ничего!
        await clear_prev_messages(message.message_id, message.chat.id, 1)
        await bot.edit_message_text(chat_id=chat_id, message_id=cur_vacancy.message_id, text=text_message,
                                    reply_markup=kb,
                                    parse_mode='html')
        if cur_vacancy.is_ready_vacancy:
            mg = await bot.send_message(chat_id=chat_id, text='/new')
            cur_vacancy.message_id = mg.message_id


@dp.callback_query_handler(lambda call: True)
async def callback_inline(cb):
    # для удобной работы с данными
    chat_id = cb.message.chat.id
    cur_vacancy = vacancy_per_user.get(chat_id, None)
    if not cur_vacancy:  # Если нет у текущего чата объекта вакансии -
        # создает новый объект и присваивает к текущему чату,
        # !*может произойти после ребута
        await bot.edit_message_text(chat_id=chat_id, message_id=cb.message.message_id, text="/start", reply_markup=None)
        await start_over(cb.message)
        return

    if cur_vacancy.start_message:  # Удаление первого сообщения с ракетами
        await bot.delete_message(chat_id=cb.message.chat.id, message_id=cur_vacancy.start_message.message_id)
        cur_vacancy.start_message = None

    cur_vacancy.update_data(cb.data)  # Работа с данными
    cur_vacancy.next_step()  # обновляет шаг + 1 проводит инициализацию след. текст и клавиатуры

    # Обновленные текст и клавиатура для шага =+ 1
    kb = cur_vacancy.cur_kb
    text_message = cur_vacancy.cur_text_for_messages

    await bot.edit_message_text(chat_id=chat_id, message_id=cur_vacancy.message_id, text=text_message,
                                reply_markup=kb, parse_mode='html')

    if cur_vacancy.is_ready_vacancy:
        mg = await bot.send_message(chat_id=chat_id, text='Вакансия создана. Введи /new')
        cur_vacancy.message_id = mg.message_id

    await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text=cb.data)


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
