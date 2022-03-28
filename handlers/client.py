from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress

from create_bot import dp, bot

from Vacancy import vacancy_per_user, Vacancy
from etc import get_exist_vacancy, chat_message_id, clear_markup


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
        except:
            print('No message to dlt')
            continue
        finally:
            counter -= 1


# приветственный текст + new_vacancy(message)
# @dp.message_handler(commands=['start', "help"])
async def command_start(message: types.Message):
    with suppress(MessageNotModified):
        """
        При старте бота
            Приветственное сообщение
            Создание новой вакансии
        :param message:
        :return: None
        """
        chat_id, mg_id = chat_message_id(message)
        await bot.send_message(chat_id,
                               text=f"Добро пожаловать, {message.from_user.full_name}! Бот поможет опубликовать вакансию на канале @uejobs. В этом сообщении вы увидите предпросмотр вашей вакансии, когда начнёте заполнять информацию",
                               reply_markup=types.ReplyKeyboardRemove())

        await command_new(message)


# создание новой вакансии
# @dp.message_handler(commands=['new'])
async def command_new(message: types.Message):
    """
    Создание новой вакансии
        Создает новое голавное сообщение и присваивает его к объекту вакансии
        Возврат в главное меню
    :param message:
    :return:
    """
    with suppress(MessageNotModified):
        chat_id, mg_id = chat_message_id(message)
        # на всякий случай очищает клавиатуры последних 2 сообщений
        await clear_markup(mg_id, chat_id)

        # Работаем с этим сообщением
        main_mg = await bot.send_message(chat_id, 'Предпросмотр...')
        cur_vacancy = Vacancy(main_mg.message_id, chat_id)

        vacancy_per_user[chat_id] = cur_vacancy
        await cur_vacancy.update_vacancy_text(chat_id, bot)

        mp = cur_vacancy.get_mp
        await cur_vacancy.update_vacancy_text(chat_id, bot)
        await bot.edit_message_reply_markup(chat_id, cur_vacancy.mg_id, reply_markup=mp)
        return cur_vacancy


# Работа с данными без клавиатуры - описание, и др., где требуется ввод с клавиатуры
# @dp.message_handler()
async def text_handler(message: types.Message):
    with suppress(MessageNotModified):
        chat_id, mg_id = chat_message_id(message)
        cur_vacancy = vacancy_per_user.get(chat_id, None)
        if cur_vacancy:
            pass
        else:
            await command_new(message)

        action = cur_vacancy.menu.menu_action()
        if action == 'text':
            cur_vacancy.info[cur_vacancy.menu.cb_tag] = message.text
            if cur_vacancy.menu.cb_tag == 'vacancy':
                await cur_vacancy.update_code_art(message.text)
            await cur_vacancy.update_vacancy_text(message.chat.id, bot)
            await menu_return(message)
            print(cur_vacancy.info)
        # удаляет сообщение пользователя, когда не надо вводить ничего!
        await delete_prev_messages(message.message_id, message.chat.id, 1)


# Меню заполнения вакансии
# @dp.callback_query_handler(lambda call: call.data == 'back_menu')
async def menu_return(cb):
    with suppress(MessageNotModified):
        vacancy = await get_exist_vacancy(cb, command_new)
        if vacancy:
            cur_vacancy, chat_id, mg_id = vacancy
        else:
            return
        # Работаем только с актуальным сообщением
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

    try:
        await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
    except Exception as err:
        print(err)


# @dp.callback_query_handler(lambda call: call.data.startswith('clear_'))
async def clear_field(cb):
    vacancy = await get_exist_vacancy(cb, command_new)
    if vacancy:
        cur_vacancy, chat_id, mg_id = vacancy
    else:
        return

    if cur_vacancy:
        if not cur_vacancy.info[cur_vacancy.menu.cb_tag] == 'Unknown' and cur_vacancy.menu.cb_tag == 'project':
            cur_vacancy.info[cur_vacancy.menu.cb_tag] = 'Unknown'
        else:
            cur_vacancy.info[cur_vacancy.menu.cb_tag] = None

        await cur_vacancy.update_vacancy_text(cb.message.chat.id, bot)
        await menu_return(cb.message)


# @dp.callback_query_handler(lambda call: call.data in ('Intern', 'Junior', 'Middle', "Senior"))
async def jun_mid_sen(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        vacancy = await get_exist_vacancy(cb, command_new)
        if vacancy:
            cur_vacancy, chat_id, mg_id = vacancy
        else:
            return

        if cur_vacancy and mg_id == cur_vacancy.mg_id:
            cur_vacancy.info['jun_mid_sen'] = cb.data
            try:
                await cur_vacancy.update_vacancy_text(chat_id, bot)
                await menu_return(cb.message)
            except Exception as err:
                print(err)
        else:
            await command_new(cb.message)

        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


# @dp.callback_query_handler(lambda call: call.data in ('Remote', 'PC', "Console", "VR/AR", "Mobile", 'Relocate'))
async def platform_cb(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        vacancy = await get_exist_vacancy(cb, command_new)
        if vacancy:
            cur_vacancy, chat_id, mg_id = vacancy
        else:
            return

        if cur_vacancy and mg_id == cur_vacancy.mg_id:
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
            await command_new(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


# @dp.callback_query_handler(lambda call: call.data in ('Full-Time', "Part-Time", "Contract"))
async def schedule(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        vacancy = await get_exist_vacancy(cb, command_new)
        if vacancy:
            cur_vacancy, chat_id, mg_id = vacancy
        else:
            return

        if cur_vacancy and mg_id == cur_vacancy.mg_id:
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
            await command_new(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


# @dp.callback_query_handler(lambda call: call.data in ("Negotiable"))
async def pay(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        vacancy = await get_exist_vacancy(cb, command_new)
        if vacancy:
            cur_vacancy, chat_id, mg_id = vacancy
        else:
            return

        if cur_vacancy and mg_id == cur_vacancy.mg_id:
            cur_vacancy.info['payment'] = "По договоренности"
            try:
                await cur_vacancy.update_vacancy_text(chat_id, bot)
                await menu_return(cb.message)
                await bot.edit_message_reply_markup(chat_id, message_id=cur_vacancy.mg_id,
                                                    reply_markup=cur_vacancy.get_mp)
            except Exception as err:
                print(err)
        else:
            await command_new(cb.message)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


# Меню заполнения вакансии
# проверка cb на тег меню
# @dp.callback_query_handler(lambda call: True)
async def callback_all(cb):
    with suppress(MessageNotModified):
        # для удобной работы с данными сообщения
        vacancy = await get_exist_vacancy(cb, command_new)
        if vacancy:
            cur_vacancy, chat_id, mg_id = vacancy
        else:
            return
        # Работаем только с актуальным сообщением
        if cur_vacancy and mg_id == cur_vacancy.mg_id:
            if cb.data in cur_vacancy.menu.children.keys():
                cur_vacancy.menu = cur_vacancy.menu.children[cb.data]
                await cur_vacancy.update_vacancy_text(cb.message.chat.id, bot)
                mp = cur_vacancy.get_mp
                try:
                    await bot.edit_message_reply_markup(chat_id, mg_id, reply_markup=mp)
                except Exception as err:
                    print(err)
        else:  # одно из предыдущий Сообщений
            try:
                await command_new(cb.message)
            except Exception as err:
                print(err)
        try:
            await bot.answer_callback_query(show_alert=False, callback_query_id=cb.id, text="Success!")
        except Exception as err:
            print(err)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_new, commands=['new'])
    dp.register_message_handler(text_handler)
    dp.register_callback_query_handler(menu_return, lambda call: call.data == 'back_menu')
    dp.register_callback_query_handler(clear_field, lambda call: call.data.startswith('clear_'))
    dp.register_callback_query_handler(jun_mid_sen,
                                       lambda call: call.data in ('Intern', 'Junior', 'Middle', "Senior"))
    dp.register_callback_query_handler(platform_cb, lambda call: call.data in (
        'Remote', 'PC', "Console", "VR/AR", "Mobile", 'Relocate'))
    dp.register_callback_query_handler(schedule, lambda call: call.data in ('Full-Time', "Part-Time", "Contract"))
    dp.register_callback_query_handler(pay, lambda call: call.data in ("Negotiable"))
    dp.register_callback_query_handler(callback_all, lambda call: True)
