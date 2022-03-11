from aiogram import types
from markup_text import text_pattern, MENU, COMMANDS

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
        self.cur_kb, self.text_for_message = None, ""
        self._is_ready_vacancy = False

        # menu, filling, history
        self.state = 'menu'
        self.start_message = None

    @property
    def is_ready_vacancy(self) -> bool:
        return self._is_ready_vacancy

    # Итоговый вывод вакансии и отправки нового сообщения для конечного для цикла
    @is_ready_vacancy.setter
    def is_ready_vacancy(self, value: bool):
        self._is_ready_vacancy = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        match value:
            case "menu":
                self._state = value
                self.cur_kb, self.text_for_message = self.get_menu()
            case "filling":
                self._state = value
                self.cur_kb, self.text_for_message = self.get_filling()
            case "history":
                pass

    # меняет state между filling / menu
    def change_state(self):
        """
        При изменении стэта надо изменить self.state, обновить клавиатуру и обновить текст
        :param:
        :return:
        """
        match self._state:
            case "menu":
                self.state = "filling"
            case "filling":
                self.state = "menu"
            case "history":
                pass
            case True:
                self.state = "menu"

    @property
    def parse_vacancy_any_stage(self):
        return ' '.join(self.info.values())

    # markup keyboard text from file markup_text.py
    @property
    def vacancy_filling_kb(self) -> types.InlineKeyboardMarkup:
        """
        Возвращает inline клавиатуру из файла markup_text.py, соответствующую текущему stage
        :return: клавиатуру, соответствующую текущему шагу
        """
        text_for_kb = text_pattern[self.cur_stage][1]
        row_width = len(text_for_kb)
        markup_data = [(i, i) for i in text_for_kb]
        return self.mp_from_tuple(markup_data)

    #  text from file markup_text.py
    @property
    def vacancy_request_text(self, other_text=None) -> str:
        """
        Возвращает текст из файла markup_text.py, соответствующий текущему stage
        :return: str
        """
        text = text_pattern[self.cur_stage][0]
        return text if not other_text else other_text

    @property
    def cur_stage(self) -> str:
        """
        Вывод названия шага по номеру шага. Если шаг больше общего количества шагов - return последний шаг
        :return:
        """
        if self.step < len(self.STAGES):
            return self.STAGES[self.step]
        else:
            return self.STAGES[-1]

    def get_menu(self):
        markup = self.mp_from_tuple(MENU[1])
        return markup, MENU[0]

    def get_filling(self) -> tuple:
        markup = self.vacancy_filling_kb
        text = self.vacancy_request_text
        return markup, text

    def update_data(self, data):
        """
        Добавляет данные для парсинга вакансии.
        :param data:
        :return:
        """
        self.info[self.cur_stage] = data

    def next_step(self):
        """Обновляет клавиатуру, текст, step создания вакансии"""
        if self.step < self.STAGES_length:
            self.step += 1

        if self.step == self.STAGES_length:
            self.text_for_message = self.parse_vacancy_any_stage
            self.cur_kb = None
            self.is_ready_vacancy = True
            return self

        self.cur_kb = self.vacancy_filling_kb
        self.text_for_message = self.vacancy_request_text
        return self

    def save_previous_vacancy(self) -> bool:
        """
        Сохраняет предыдущую готовую вакансию в буффер - рассчитан на 2 вакансии
        :return:
        """
        pass

    @staticmethod
    def mp_from_tuple(data_tuples: tuple) -> types.InlineKeyboardMarkup:
        """
        Создает клавиатуру из кортежа данных

        :type data_tuples: tuple[tuple,]
        :param data_tuples: (text, call_back_tag)
        :return: inline keyboard markup
        """
        mp_width = len(data_tuples)
        mp = types.InlineKeyboardMarkup(row_width=mp_width)
        for i in range(mp_width):
            text, cb = data_tuples[i]
            item = types.InlineKeyboardButton(text, callback_data=cb)
            mp.add(item)
        return mp
