import logging
from aiogram import Bot, Dispatcher, executor

import mytoken
from Vacancy import vacancy_per_user, Vacancy, types
from testing.sqllighter3 import SQLighter

logging.basicConfig(level=logging.INFO)

# Bot init
bot = Bot(token=mytoken.TOKEN)
dp = Dispatcher(bot)
db = SQLighter('db.db')


# Команды для старта или создания новой вакансии
@dp.message_handler(commands=['new', 'start'])
async def start_over(message: types.Message):
    vacancy_per_user[message.chat.id] = Vacancy()
    text = vacancy_per_user[message.chat.id].get_text_per_stage()
    markup = vacancy_per_user[message.chat.id].get_markup()
    await bot.send_message(message.chat.id, "🚀 Starting", reply_markup=None)
    await bot.send_message(message.chat.id, text, reply_markup=markup)


# Вывод текущего шага создания вакансии
@dp.message_handler(commands=['current'])
async def show_current_stage(message: types.Message):
    await bot.send_message(message.chat.id, str(f'You are at: '))


@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message):
    # Если вакансии не было - создает новую, или возвращает существующую
    vacancy_per_user.setdefault(message.chat.id, Vacancy())
    vacancy_obj = vacancy_per_user[message.chat.id]

    # Если текущий шаг меньше массива всех шагов
    if vacancy_obj.stage < len(vacancy_obj.STAGES):
        vacancy_obj.info[vacancy_obj.STAGES[vacancy_obj.stage]] = message.text.strip()

        vacancy_obj.stage += 1

        # Дополнительная проверка - текущий шаг может быть больше длины массива
        if vacancy_obj.stage < len(vacancy_obj.STAGES):
            await bot.send_message(message.chat.id, vacancy_obj.get_text_per_stage(), reply_markup=vacancy_obj.get_markup())
    # Если текущий шаг равен массиву шагов
    if vacancy_obj.stage == len(vacancy_obj.STAGES):
        # Добавляем клавиутуру для создания новой вакансии
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton('/new'))
        await bot.send_message(message.chat.id, vacancy_obj.get_ready_vacancy(),
                               reply_markup=markup, parse_mode='html')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
