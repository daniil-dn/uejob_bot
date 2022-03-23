from collections import OrderedDict

from aiogram import types, Bot
from markup_text import text_pattern, USER_MENU, MENU_ACTIONS, MP_WIDTH

vacancy_per_user = {}


class Vacancy:

    def __init__(self, main_mg_id, chat_id):
        """
        Создает new объект вакансии.
        Инициализирует Шаги из файлы markup_text.py

        :param main_mg_id:
        :param chat_id:
        """
        self.mg_id = main_mg_id
        self.chat_id = chat_id

        self.info = {}

        # по дефолту попадаем в корень меню
        self.menu = self.render_menu(USER_MENU)

    @property
    def parse_vacancy_any_stage(self):
        return ' '.join(self.info.values())

    @property
    def get_mp(self):
        row_width = self.menu.row_width
        children_len = len(self.menu.children)
        action = MENU_ACTIONS.get(self.menu.cb_tag, MENU_ACTIONS['all'])

        mp = types.InlineKeyboardMarkup(row_width=row_width)

        counter = 0
        cache = []
        for tag, next_menu in self.menu.children.items():
            cache.append(types.InlineKeyboardButton(next_menu.text, callback_data=tag))
            counter += 1
            if counter % row_width == 0 or counter == len(self.menu.children):
                mp.add(*cache)
                cache = list()

        # для sub_menu всегда выводит кнопку Назад
        if not self.menu.parent == 'root':
            mp.add(self.menu.back_button())
        return mp

    async def update_vacancy_text(self, chat_id, bot: Bot):
        """

        :param chat_id:
        :param bot:
        :return:
        """
        if self.info:

            text = f"""
{self.tags()}
{self.vacancy_title()} {self.company()}
            
{self.project()} {self.platform()}
{self.experience()}
{self.payment()}
{self.schedule()}
{self.location()}
            
{self.description()}
            
{self.duty()}
{self.skills()}
{self.add_skills()}
{self.conditions()}
{self.useful_info()}
{self.contacts()}
            """
            # text = str(self.info)

            try:
                await bot.edit_message_text(text, chat_id, self.mg_id)
            except Exception as err:
                print(err)

    def tags(self):
        return ""

    def vacancy_title(self):
        return self.info.get('vacancy', '')

    def company(self, is_tag=False):
        return self.info.get('company', '')

    def project(self):
        return self.info.get('project', '')

    def platform(self, is_tag=False):
        return self.info.get('platform', '')

    def experience(self, is_tag=False):
        return self.info.get('jun_mid_sen', '') + self.info.get('years', '')

    def schedule(self, is_tag=False):
        return self.info.get('schedule', '')

    def payment(self):
        return self.info.get('payment', '')

    def location(self, is_tag=False):
        return self.info.get('location', '')

    def description(self, is_tag=False):
        return self.info.get('description', '')

    def duty(self):
        return self.info.get('duty', '')

    def skills(self):
        return self.info.get('skills', '')

    def add_skills(self):
        return self.info.get('add_skills', '')

    def conditions(self):
        return self.info.get('conditions', '')

    def useful_info(self):
        return self.info.get('useful_info', '')

    def contacts(self):
        return self.info.get('contacts', '')

    @staticmethod
    def render_menu(menu_dict: OrderedDict = USER_MENU):
        root_menu = MenuItem(parent='root', children_dict=menu_dict)
        return root_menu

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


class MenuItem:
    def __init__(self, cb_tag='root', text=None, parent=None, children_dict: OrderedDict = None):
        self.parent = parent
        self.text = text
        self.cb_tag = cb_tag
        self.children = {}

        # создание дерева меню
        # с помощью рекурсии создаются элементы меню(ноды), связанные с предыддущим элементом.
        if isinstance(children_dict, dict):
            for tag, value in children_dict.items():
                if isinstance(value, tuple):
                    self.children[tag] = MenuItem(tag, value[0], self, value[1])
                else:
                    self.children[tag] = MenuItem(tag, value, self)

    def __str__(self):
        return str(self.children)

    @property
    def row_width(self):
        return MP_WIDTH.get(self.cb_tag, MP_WIDTH['all'])

    def menu_action(self, MENU_ACTIONS: dict = MENU_ACTIONS):
        if self.cb_tag in MENU_ACTIONS['nothing_exceptions']:
            return 'nothing'
        else:
            return MENU_ACTIONS.get(self.cb_tag, MENU_ACTIONS['all'])

    def back_menu(self):
        # Возвращает предыдущее меню, если это не root меню
        return self.parent if self.parent != 'root' else None

    def back_mp(self):
        mp = types.InlineKeyboardMarkup(row_width=1)
        mp.add(self.back_button())
        return mp

    def back_button(self):
        return types.InlineKeyboardButton("Назад", callback_data='back_menu')
