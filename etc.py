import logging

from aiogram import types
from Vacancy import vacancy_per_user
from create_bot import bot


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


async def get_exist_vacancy(message, to_do_else=None) -> tuple | None:
    chat_id, mg_id = chat_message_id(message)
    cur_vacancy = vacancy_per_user.get(chat_id, None)
    action = ''
    if type(message) is types.CallbackQuery:
        message = message.message
    else:
        action = cur_vacancy.menu.menu_action()

    if cur_vacancy and mg_id == cur_vacancy.mg_id or action == 'text':
        return cur_vacancy, chat_id, mg_id
    else:
        if to_do_else:
            try:
                await to_do_else(message)
                return
            except Exception as err:
                logging.log(err)

