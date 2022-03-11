from aiogram import types
from markup_text import text_pattern

vacancy_per_user = {}


class Vacancy:
    def __init__(self, message_id, chat_id):
        """
        Создает new объект вакансии.
        Инициализирует Шаги из файлы markup_text.py

        :param message_id:
        :param chat_id:
        """
        self.step = 0
        self.message_id = message_id
        self.chat_id = chat_id
        self.STAGES = [s for s in text_pattern]
        self.STAGES_length = len(self.STAGES)
        self.info = {}
        self.cur_kb = self.inline_kb()
        self.cur_text_for_message = self.get_reply_text()
        self._is_ready_vacancy = False

    @property
    def is_ready_vacancy(self) -> bool:
        return self._is_ready_vacancy

    @is_ready_vacancy.setter
    def is_ready_vacancy(self, value: bool):
        self._is_ready_vacancy = value

    def get_menu(self):
        return str(self.info)

    def update_data(self, data):
        """
        Обновляет текущие данные для парсинга вакансии.
        Обновляет шаг, клавиатуру, текст для запроса данных.
        :param data:
        :return:
        """
        self.info[self.cur_stage] = data
        return self

    def next_step(self):
        """Обновляет клавиатуру, текст, step создания вакансии"""
        if self.step < self.STAGES_length:
            self.step += 1

        if self.step == self.STAGES_length:
            self.cur_text_for_message = self.parse_vacancy_any_stage()
            self.cur_kb = None
            self.is_ready_vacancy = True
            return self

        self.cur_kb = self.inline_kb()
        self.cur_text_for_message = self.get_reply_text()
        return self

    def parse_vacancy_any_stage(self):
        return ' '.join(self.info.values())

    def inline_kb(self) -> types.InlineKeyboardMarkup | None:  # TODO сделать дескриптор на проверку последнего шага
        """
        Возвращает inline клавиатуру из файла markup_text.py, соответствующую текущему stage
        :return: клавиатуру, соответствующую текущему шагу
        """
        text_for_kb = text_pattern[self.cur_stage][1]
        row_width = len(text_for_kb)
        markup = types.InlineKeyboardMarkup(row_width=row_width)
        for item in range(row_width):
            i = types.InlineKeyboardButton(text_for_kb[item], callback_data=text_for_kb[item])
            markup.add(i)
        return markup

    def get_reply_text(self, other_text=None) -> str:
        """
        Возвращает текст из файла markup_text.py, соответствующий текущему stage
        :return: str
        """
        text = text_pattern[self.cur_stage][0]
        return text if not other_text else other_text

    @property
    def cur_stage(self) -> str:
        if self.step < len(self.STAGES):
            return self.STAGES[self.step]
        else:
            return self.STAGES[-1]

    # todo
    def save_previous_vacancy(self) -> bool:
        """
        Сохраняет предыдущую готовую вакансию в буффер - рассчитан на 2 вакансии
        :return:
        """
        pass
