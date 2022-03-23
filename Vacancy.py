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
        self.info['payment'] = "По договоренности"
        self.info['schedule'] = "Full-Time"
        self.info['jun_mid_sen'] = 'Middle'

        # по дефолту попадаем в корень меню
        self.menu = self.render_menu(USER_MENU)

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
            text = self.tags() + '\n\n'
            text += "<b>" + self.vacancy_title() + self.company() + "</b>" + '\n\n' \
                    + self.project() + self.platform() + '\n' \
                    + '🧠 ' + self.jun_mid_sen() + self.experience() + '\n' \
                    + self.payment() \
                    + self.schedule() \
                    + self.location() \
                    + self.description() \
                    + self.duty() \
                    + self.skills() \
                    + self.add_skills() \
                    + self.conditions() \
                    + self.useful_info() \
                    + self.contacts()
            print(self.vacancy_title())
            print(self.company())
            try:
                await bot.edit_message_text(text, chat_id, self.mg_id, parse_mode="html")
            except Exception as err:
                print(err)

    def tags(self):
        """
        #UnrealEngine #GameDev #FullTime #Art #Middle #PC #Remote #Office #ProgramAce

        :return:
        """
        tags = "#UnrealEngine #GameDev "
        tags += self.schedule(is_tag=True)
        tags += self.art_code()

        tags += self.jun_mid_sen(is_tag=True)
        tags += self.platform(is_tag=True)

        tags += self.location(is_tag=True)
        tags += self.company(is_tag=True)

        return tags

    def art_code(self):
        art_code_var = self.info.get('art_code', '')
        return f"#{art_code_var.capitalize()} " if art_code_var else ''

    def jun_mid_sen(self, is_tag=False):

        jun_mid_sen = self.info.get('jun_mid_sen', '')
        if is_tag:
            return f"#{jun_mid_sen} " if jun_mid_sen else ''
        else:
            return f"{jun_mid_sen} " if jun_mid_sen else ''

    def vacancy_title(self):
        title = self.info.get('vacancy', '')
        result = self.jun_mid_sen() + "UNREAL ENGINE " + title
        return result.upper() + ' ' if title else result.upper()

    def company(self, is_tag=False):
        company = self.info.get('company', '')

        if is_tag and company:
            return f"#{company.title().replace(' ', '').replace('-', '')} "

        if not is_tag and company:
            company = company.capitalize() if company and company[0].islower() else company
            return f'({company})'
        return ''

    def project(self):
        name = self.info.get('project', 'Unknown ')
        return '🕹 ' + name.capitalize()

    def platform(self, is_tag=False):
        pc = self.info.get('PC', None)
        console = self.info.get('Console', None)
        vr = self.info.get('VR', None)
        mobile = self.info.get('Mobile', None)

        if is_tag:
            pc = f'#{pc} ' if pc else ''
            console = f'#{console} ' if console else ''
            vr = f'#{vr} ' if vr else ''
            mobile = f'#{mobile} ' if mobile else ''
            result = pc + console + vr + mobile

        else:
            to_join = []
            for i in (pc, console, vr, mobile):
                if i:
                    to_join.append(i)
            result = ', '.join(to_join)
            result = f'({result})'

        return result

    def experience(self, is_tag=False):
        years = self.info.get('years', '')
        return f"({years}+)" if years else ""

    def schedule(self, is_tag=False):
        schedule = self.info.get('schedule', '')
        if is_tag and schedule:
            return f'#{schedule.replace("-", "")} '
        elif schedule:
            return f"⏰ {schedule} \n"
        else:
            return ''

    def payment(self):
        return f"💰 {self.info.get('payment', '')}\n"

    def location(self, is_tag=False):
        remote = self.info.get('Remote', None)
        office = self.info.get('Office', None)

        if is_tag:
            remote = f'#Remote ' if remote else ''
            office = '#Office ' if office else ''
            result = remote + office
        else:
            remote = f'🌎 Удаленно' if remote else ''
            office = f'👔 Офис ({office})' if office else ''
            if remote and office:
                result = f"{remote} || {office}" + "\n\n"
            else:
                result = remote + office + "\n\n"
        return result

    def description(self):
        desc = self.info.get('description', '')
        return f'🦄 {desc} \n\n' if desc else ''

    def duty(self):
        duty = self.info.get('duty', '')
        return f'<b>🚀 Что ты будешь делать</b>{self.to_bullet(duty)}\n\n' if duty else ''

    def skills(self):
        skills = self.info.get('skills', '')
        return f'<b>📚 Твои скиллы</b>{self.to_bullet(skills)}\n\n' if skills else ''

    def add_skills(self):
        add_skills = self.info.get('add_skills', '')
        return f'<b>👍 Круто, если знаешь</b>{self.to_bullet(add_skills)}\n\n' if add_skills else ''

    def conditions(self):
        cond = self.info.get('conditions', '')
        return f'<b>🍪 Условия и плюшки</b>{self.to_bullet(cond)}\n\n' if cond else ''

    def useful_info(self):
        useful_info = self.info.get('useful_info', '')
        return f'<b>ℹ️ Полезная информация</b>{self.to_bullet(useful_info)}\n\n' if useful_info else ''

    def contacts(self):
        contacts = self.info.get('contacts', '')

        return f'<b>📨 Контакты</b>\n{contacts}\nVacancy here 👌' if contacts else ''

    @staticmethod
    def to_bullet(text: str, splitter: str = '='):
        if text[0] in ('=') or text[1] in ('='):
            list_items = text.split('=')
        else:
            list_items = text.splitlines()
        result = ''

        list_items = list(map(str.strip, list_items))
        for item in list_items:
            if item:
                result += '\n• ' + item.replace(';', '').replace('·', '').replace('•', '').strip('•').strip('-').strip(). strip('.')
        return result

    @staticmethod
    def render_menu(menu_dict: OrderedDict = USER_MENU):
        root_menu = MenuItem(parent='root', children_dict=menu_dict)
        return root_menu

    @staticmethod
    def mp_from_tuple(data_tuples: tuple) -> types.InlineKeyboardMarkup:
        """
            Создает
            клавиатуру
            из
            кортежа
            данных

            : type
            data_tuples: tuple[tuple,]
            :param
            data_tuples: (text, call_back_tag)
            :return: inline
            keyboard
            markup
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
        return self.parent if self.parent != 'root' else self

    def back_mp(self):
        mp = types.InlineKeyboardMarkup(row_width=1)
        mp.add(self.back_button())
        return mp

    def back_button(self):
        return types.InlineKeyboardButton("Назад", callback_data='back_menu')
