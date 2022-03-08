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
        self.step = -1
        self.message_id = message_id
        self.chat_id = chat_id
        self.STAGES = []
        for s in text_pattern:
            self.STAGES.append(s)
        self.info = []

    def update_data(self, data):
        """
        Обновляет текущие данные для парсинга вакансии.
        Обновляет шаг, клавиатуру, текст для запроса данных.
        :param data:
        :return:
        """
        cur_step_str = self.STAGES[self.step]
        match cur_step_str:
            case 'vacancy_title':
                pass
        return self.next_step()

    def next_step(self):
        """Обновляет клавиатуру, текст, step создания вакансии"""
        self.step += 1
        self.cur_kb = self.get_inline_kb()
        self.cur_text_for_message = self.get_reply_text()
        return self

    # todo
    def save_previous_vacancy(self) -> bool:
        """
        Сохраняет предыдущую готовую вакансию в буффер - рассчитан на 2 вакансии
        :return:
        """
        pass

    def get_inline_kb(self) -> types.InlineKeyboardMarkup | None:  # TODO сделать дескриптор на проверку последнего шага

        """
        Возвращает inline клавиатуру из файла markup_text.py, соответствующую текущему stage

        :return: клавиатуру, соответствующую текущему шагу
        """

        if self.step >= len(self.STAGES):
            return None
        text_for_kb = text_pattern[self.STAGES[self.step]][1]
        row_width = len(text_for_kb)
        markup = types.InlineKeyboardMarkup(row_width=row_width)
        for item in range(row_width):
            i = types.InlineKeyboardButton(text_for_kb[item], callback_data=text_for_kb[item])
            markup.add(i)
        return markup

    def get_reply_text(self) -> str:
        """
        Возвращает текст из файла markup_text.py, соответствующий текущему stage
        :return: str
        """
        if self.step >= len(self.STAGES):
            return "/new"
        text = text_pattern[self.STAGES[self.step]][0]
        return text

    def get_vacancy_title(self):
        pass

    def get_skill_level(self, is_tag):
        pass

    def get_company_name(self, is_tag):
        pass

    def get_game_title(self):
        pass

    def get_art_code(self, is_tag, auto_code=True):
        pass

    def get_years(self):
        pass

    def platform(self, is_tag):
        pass

    def get_remote(self, is_tag):
        pass

    def get_office(self, is_tag):
        pass

    def get_location(self):
        pass

    def get_money_parsed(self):
        pass

    def get_schedule(self, default='FullTime'):
        pass

    def get_description(self):
        pass

    def get_bullet(self, splitter='='):
        pass

    def get_contact(self):
        pass
