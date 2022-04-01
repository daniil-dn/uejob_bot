import logging

from aiogram import Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.utils.executor import start_webhook

from mytoken import TOKEN as API_TOKEN
from Vacancy import vacancy_per_user, Vacancy, types
from markup_text import help_text, WHERE_SEND, AFTER_SEND_MP, AFTER_SEND_ALERT, WEBHOOK_HOST, WEBAPP_HOST, WEBAPP_PORT

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
    with suppress(MessageNotModified):
        """
        При старте бота
            Приветственное сообщение
            Создание новой вакансии
        :param message:
        :return: None
        """
        chat_id, mg_id = chat_message_id(message)

        await new_vacancy(message)


@dp.message_handler(commands=['new'])
@dp.callback_query_handler(lambda call: call.data.startswith('/new'))
async def new_vacancy(message: types.Message):
    """
    Создание новой вакансии
        Создает новое голавное сообщение и присваивает его к объекту вакансии
        Возврат в главное меню
    :param message:
    :return:
    """
    if type(message) is types.CallbackQuery:
        message = message.message
    with suppress(MessageNotModified):
        chat_id, mg_id = chat_message_id(message)
        # на всякий случай очищает клавиатуры последних 2 сообщений
        await clear_markup(mg_id, chat_id)

        # Работаем с этим сообщением
        mg = await bot.send_message(chat_id, disable_web_page_preview=True,
                                    text=help_text['start'].format(name=message.chat.first_name))

        cur_vacancy = Vacancy(mg.message_id, chat_id, user_name=message.chat.first_name)

        vacancy_per_user[chat_id] = cur_vacancy
        await cur_vacancy.update_vacancy_text(chat_id, bot)

        mp = cur_vacancy.get_mp
        await bot.edit_message_reply_markup(chat_id, cur_vacancy.mg_id, reply_markup=mp)
        return cur_vacancy


# Работа с данными без клавиатуры - описание, и др., где требуется ввод с клавиатуры
@dp.message_handler()
async def text_handler(message: types.Message):
    with suppress(MessageNotModified):
        chat_id, cb_mg_id = chat_message_id(message)
        cur_vacancy = vacancy_per_user.get(chat_id, None)

        if cur_vacancy:
            action = cur_vacancy.menu.menu_action()

            if action == 'text':
                cur_vacancy.info[cur_vacancy.menu.cb_tag] = message.text[0:1000]

                await cur_vacancy.update_code_art(message.text)
                await cur_vacancy.update_vacancy_text(message.chat.id, bot)
                await menu_return(message)
            # удаляет сообщение пользователя, когда не надо вводить ничего!
            await delete_prev_messages(message.message_id, message.chat.id, 1)


# Меню заполнения вакансии
@dp.callback_query_handler(lambda call: call.data == 'back_menu')
async def menu_return(cb):
    with suppress(MessageNotModified):
        try:
            chat_id, cb_mg_id = chat_message_id(cb)
            cur_vacancy = vacancy_per_user.get(chat_id, None)
            if not cur_vacancy:
                cur_vacancy = await new_vacancy(cb.message)

            # Работаем только с актуальным сообщением
            if cb_mg_id == cur_vacancy.mg_id or type(cb) is types.Message:
                try:
                    cur_vacancy.menu = cur_vacancy.menu.back_menu()
                    await cur_vacancy.update_vacancy_text(chat_id, bot)
                except Exception as err:
                    print(err)
                mp = cur_vacancy.get_mp
                try:
                    await bot.edit_message_reply_markup(chat_id, cur_vacancy.mg_id, reply_markup=mp)
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)
            print('back')


@dp.callback_query_handler(lambda call: call.data.startswith('clear_'))
async def clear_field(cb):
    chat_id, cb_mg_id = chat_message_id(cb)
    cur_vacancy = vacancy_per_user.get(chat_id, None)

    if cur_vacancy:
        if 'Unknown' in cb.data:
            cur_vacancy.info[cur_vacancy.menu.cb_tag] = 'Unknown'
        elif cur_vacancy.menu.cb_tag == 'project':
            try:

                for i in ('PC', "Console", "VR/AR", "Mobile"):
                    if cur_vacancy.info.get(i):
                        del cur_vacancy.info[i]
                del cur_vacancy.info[cur_vacancy.menu.cb_tag]
            except Exception as err:
                print(err)
        elif cur_vacancy.menu.cb_tag == 'contacts':
            try:
                del cur_vacancy.info[cur_vacancy.menu.cb_tag]

            except Exception as err:
                try:
                    del cur_vacancy.info['vacancy_link']
                except Exception as err:
                    print(err)

        else:
            try:
                del cur_vacancy.info[cur_vacancy.menu.cb_tag]
            except Exception as err:
                print(err)

        await cur_vacancy.update_vacancy_text(cb.message.chat.id, bot)
        await menu_return(cb.message)


@dp.callback_query_handler(lambda call: call.data in ('Intern', 'Junior', 'Middle', "Senior"))
async def jun_mid_sen(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        chat_id, cb_mg_id = chat_message_id(cb)

        cur_vacancy = vacancy_per_user.get(chat_id, None)

        if cur_vacancy and cb_mg_id == cur_vacancy.mg_id:
            if cur_vacancy.info.get(cb.data, None):
                del cur_vacancy.info[cb.data]
                await cur_vacancy.update_vacancy_text(chat_id, bot)
            else:
                cur_vacancy.info[cb.data] = cb.data
                await cur_vacancy.update_vacancy_text(chat_id, bot)
            try:
                await cur_vacancy.update_vacancy_text(chat_id, bot)
                # await menu_return(cb.message)\
                await bot.edit_message_reply_markup(chat_id, message_id=cur_vacancy.mg_id,
                                                    reply_markup=cur_vacancy.get_mp)
            except Exception as err:
                print(err)
        else:
            await new_vacancy(cb.message)

        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


@dp.callback_query_handler(
    lambda call: call.data in ('Remote', 'PC', "Console", "VR/AR", "Mobile", 'Relocate'))
async def platform_cb(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        chat_id, cb_mg_id = chat_message_id(cb)

        cur_vacancy = vacancy_per_user.get(chat_id, None)

        if cur_vacancy and cb_mg_id == cur_vacancy.mg_id:
            if not cur_vacancy.info.get(cb.data, None):
                cur_vacancy.info[cb.data] = cb.data
            else:
                cur_vacancy.info[cb.data] = None
            try:
                await cur_vacancy.update_vacancy_text(chat_id, bot)
                await bot.edit_message_reply_markup(chat_id, message_id=cur_vacancy.mg_id,
                                                    reply_markup=cur_vacancy.get_mp)
            except Exception as err:
                print(err)
        else:
            await new_vacancy(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


@dp.callback_query_handler(
    lambda call: call.data in ('Full-Time', "Part-Time", "Contract"))
async def schedule(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        chat_id, cb_mg_id = chat_message_id(cb)

        cur_vacancy = vacancy_per_user.get(chat_id, None)

        if cur_vacancy and cb_mg_id == cur_vacancy.mg_id:
            if not cur_vacancy.info.get(cb.data, None):
                cur_vacancy.info['schedule'] = cb.data
            else:
                cur_vacancy.info['schedule'] = None
            try:
                await cur_vacancy.update_vacancy_text(chat_id, bot)
                await menu_return(cb.message)
                await bot.edit_message_reply_markup(chat_id, message_id=cur_vacancy.mg_id,
                                                    reply_markup=cur_vacancy.get_mp)
            except Exception as err:
                print(err)
        else:
            await new_vacancy(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


@dp.callback_query_handler(
    lambda call: call.data in ("send_verif"))
async def send_verif(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        chat_id, cb_mg_id = chat_message_id(cb)

        cur_vacancy = vacancy_per_user.get(chat_id, None)

        if cur_vacancy and cb_mg_id == cur_vacancy.mg_id:
            try:
                text = await cur_vacancy.update_vacancy_text(chat_id, bot, is_send=True)
                await bot.send_message(chat_id=WHERE_SEND, text=text, parse_mode="html", disable_web_page_preview=True)
                await bot.answer_callback_query(show_alert=True, callback_query_id=cb.id,
                                                text=AFTER_SEND_ALERT)

                mp = cur_vacancy.mp_from_tuple(AFTER_SEND_MP)
                await bot.edit_message_reply_markup(chat_id, message_id=cur_vacancy.mg_id,
                                                    reply_markup=mp)

            except Exception as err:
                print(err)
        else:
            await new_vacancy(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


@dp.callback_query_handler(
    lambda call: call.data in ("reset_verif"))
async def reset_verif(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        chat_id, cb_mg_id = chat_message_id(cb)

        cur_vacancy = vacancy_per_user.get(chat_id, None)

        if cur_vacancy and cb_mg_id == cur_vacancy.mg_id:
            try:
                await cur_vacancy.update_vacancy_text(chat_id, bot, is_send=True)
                await new_vacancy(cb.message)

            except Exception as err:
                print(err)
        else:
            await new_vacancy(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


@dp.callback_query_handler(
    lambda call: call.data in ("Negotiable"))
async def pay(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        chat_id, cb_mg_id = chat_message_id(cb)

        cur_vacancy = vacancy_per_user.get(chat_id, None)

        if cur_vacancy and cb_mg_id == cur_vacancy.mg_id:
            cur_vacancy.info['payment'] = "По договоренности"
            try:
                await cur_vacancy.update_vacancy_text(chat_id, bot)
                await menu_return(cb.message)
                await bot.edit_message_reply_markup(chat_id, message_id=cur_vacancy.mg_id,
                                                    reply_markup=cur_vacancy.get_mp)
            except Exception as err:
                print(err)
        else:
            await new_vacancy(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


# Меню заполнения вакансии
# проверка cb на тег меню
@dp.callback_query_handler(lambda call: True)
async def callback4_all(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        chat_id, cb_mg_id = chat_message_id(cb)

        cur_vacancy = vacancy_per_user.get(chat_id, None)
        # Работаем только с актуальным сообщением
        if cur_vacancy and cb_mg_id == cur_vacancy.mg_id:
            if cb.data in cur_vacancy.menu.children.keys():
                if not cur_vacancy.info and cb.data in ("pre_reset_vacancy", "pre_send_vacancy"):
                    try:
                        await bot.answer_callback_query(show_alert=True, callback_query_id=cb.id, text="Вакансия пуста")
                        return
                    except Exception as err:
                        print(err)

                cur_vacancy.menu = cur_vacancy.menu.children[cb.data]
                await cur_vacancy.update_vacancy_text(cb.message.chat.id, bot)
                mp = cur_vacancy.get_mp
                try:
                    await bot.edit_message_reply_markup(chat_id, cb_mg_id, reply_markup=mp)
                except Exception as err:
                    print(err)
        else:  # одно из предыдущий Сообщений
            try:
                await new_vacancy(cb.message)
            except Exception as err:
                print(err)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


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
