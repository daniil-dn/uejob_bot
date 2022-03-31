from collections import OrderedDict
from typing import Tuple

from aiogram import types, Bot
from aiogram.types import InlineKeyboardButton

import markup_text
from markup_text import USER_MENU, MENU_ACTIONS, MP_WIDTH, CODE_PATTERN, ART_PATTERN

vacancy_per_user = {}


class Vacancy:

    def __init__(self, main_mg_id, chat_id, user_name=''):
        """
        Создает new объект вакансии.
        Инициализирует Шаги из файлы markup_text.py

        :param main_mg_id:
        :param chat_id:
        """
        self.mg_id = main_mg_id
        self.chat_id = chat_id
        self.user_name = user_name

        self.info = {}

        self.is_art = None
        self.is_code = None

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
        cache_bottom = []
        for tag, next_menu in self.menu.children.items():
            if not tag in ('pre_send_vacancy', "pre_reset_vacancy"):
                cache.append(types.InlineKeyboardButton(next_menu.text, callback_data=tag))
            else:
                cache_bottom.append(types.InlineKeyboardButton(next_menu.text, callback_data=tag))
                # print(tag)
            counter += 1
            if counter % row_width == 0 or counter == len(self.menu.children):
                mp.add(*cache)
                cache = list()
        mp.row(*cache_bottom)

        if self.menu.cb_tag == "project" and self.info.get('project', '') != 'Unknown':
            mp.add(types.InlineKeyboardButton(f"Unknown project", callback_data=f'clear_Unknown'))
        if not self.menu.cb_tag in MENU_ACTIONS['nothing_exceptions'].split(', ') and not self.menu.cb_tag in \
                                                                                          MENU_ACTIONS[
                                                                                              'not_clear'].split(', '):
            # mp.add(types.InlineKeyboardButton(f"👇👇{self.menu.text}👇👇", callback_data='None'))
            mp.add(types.InlineKeyboardButton(f"Очистить поле", callback_data=f'clear_'))
        # для sub_menu всегда выводит кнопку Назад
        if not self.menu.parent == 'root':
            mp.add(self.menu.back_button())
        # if self.menu.cb_tag == 'root':
        #     mp.row(*self.bottom_menu_send_reset())

        return mp

    async def update_vacancy_text(self, chat_id, bot: Bot, is_send=False):
        cur_menu = f"<i>{self.menu.text}</i>" if self.menu.cb_tag != 'root' else ''
        """

        :param chat_id:
        :param bot:
        :return:
        """
        self.update_root_checked_items()
        self.update_platform_checked_items()
        self.update_remote_checked_items()
        self.update_schedule_checked_items()
        self.update_experience_checked_items()
        if self.info or True:
            tags = self.tags()
            text = self.vacancy_title() \
                   + self.project() \
                   + self.jun_mid_sen() \
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

            # отправка в канал
            if is_send:
                return tags + text + self.vacancy_link(is_preview=False)
            text += self.vacancy_link(is_preview=True)
            try:
                # Если мы в руте и нет данных
                if not self.info and self.menu.cb_tag == 'root':
                    text += self.help('start').format(name=self.user_name)
                    await bot.edit_message_text(text, chat_id, self.mg_id, parse_mode="html")

                elif self.menu.cb_tag == 'pre_send_vacancy' or is_send is True:
                    await bot.edit_message_text(text, chat_id, self.mg_id, parse_mode="html")
                elif self.menu.parent != 'root':
                    text = ''
                    match self.menu.cb_tag.lower():
                        case "company":
                            text += '<b>' + self.company().strip('()') + '</b>'
                        case "vacancy":
                            text += self.vacancy_title()
                        case "description":
                            text += self.description()
                        case "project":
                            text += self.project()
                        case "experience":
                            text += self.jun_mid_sen()
                        case "schedule":
                            text += self.schedule()
                        case "payment":
                            text += self.payment()
                        case "location" | 'office':
                            text += self.location()
                        case "duty":
                            text += self.duty()
                        case "skills":
                            text += self.skills()
                        case "add_skills":
                            text += self.add_skills()
                        case "conditions":
                            text += self.conditions()
                        case "useful_info":
                            text += self.useful_info()
                        case "contacts" | 'vacancy_link':
                            text += self.contacts() + self.vacancy_link(is_preview=True)
                    text = text.strip('/n')
                    text += self.help()
                    if text == '':
                        text = cur_menu
                    await bot.edit_message_text(text, chat_id, self.mg_id, parse_mode="html")
                else:
                    text += self.help() + cur_menu
                    await bot.edit_message_text(text, chat_id, self.mg_id, parse_mode="html")
            except Exception as err:
                print(err)

    async def update_code_art(self, text: str):
        text = text.lower()
        code_list = CODE_PATTERN
        art_list = ART_PATTERN
        self.is_code = False
        self.is_art = False

        for i in code_list:
            if i in text:
                self.is_code = True
        for i in art_list:
            if i in text:
                self.is_art = True

    def update_root_checked_items(self):
        root: MenuItem = self.menu
        while True:  # Получаем рут меню
            root = root.parent if type(root.parent) is not str else root
            if root.parent == 'root':
                break
        # print(root)
        if self.vacancy_link() == '':
            tag = 'vacancy_link'
            vacancy_link = root.children['contacts'].children[tag]
            emo = '🌐'
            vacancy_link.text = emo + vacancy_link.text[1:]
        else:
            tag = 'vacancy_link'
            vacancy_link = root.children['contacts'].children[tag]
            vacancy_link.text = "✅" + vacancy_link.text[1:]
        for k, v in root.children.items():
            emo = USER_MENU[k][0] if type(USER_MENU[k]) is str else USER_MENU[k][0][0]
            if self.info.get(k, '') or k == 'location' or k == 'experience':
                if self.platform(is_tag=True) == '' and k == 'project':
                    root.children[k].text = emo + root.children[k].text[1:]
                elif self.location(is_tag=True) == '' and k == 'location':
                    root.children[k].text = emo + root.children[k].text[1:]
                elif self.vacancy_link() == '' and k == 'vacancy_link':
                    root.children[k].text = emo + root.children[k].text[1:]
                elif self.jun_mid_sen(is_tag=True) == '' and k == 'experience':
                    root.children[k].text = emo + root.children[k].text[1:]
                else:
                    root.children[k].text = "✅" + root.children[k].text[1:]

            else:
                # print(emo)
                root.children[k].text = emo + root.children[k].text[1:]

    def update_platform_checked_items(self):
        platform: MenuItem = self.menu
        if platform.cb_tag == 'project':
            for k, v in platform.children.items():
                if platform.children[k].text.find("✅") == -1:
                    starts_with = 0
                else:
                    starts_with = 1

                if self.info.get(k, '') and k.lower() in 'pc console vr/ar mobile':
                    platform.children[k].text = "✅" + platform.children[k].text[starts_with:]
                else:
                    platform.children[k].text = platform.children[k].text[starts_with:]

    def update_remote_checked_items(self):
        location: MenuItem = self.menu
        if location.cb_tag == 'location':
            for k, v in location.children.items():
                # print(k)
                if location.children[k].text.find("✅") == -1:
                    starts_with = 0
                else:
                    starts_with = 1
                if self.info.get(k, ''):
                    location.children[k].text = "✅" + location.children[k].text[starts_with:]
                else:
                    location.children[k].text = location.children[k].text[starts_with:]

    def update_schedule_checked_items(self):
        schedule: MenuItem = self.menu
        if schedule.cb_tag == 'schedule':
            for k, v in schedule.children.items():
                if schedule.children[k].text.find("✅") == -1:
                    starts_with = 0
                else:
                    starts_with = 1

                if self.info.get('schedule', '') == k:
                    schedule.children[k].text = "✅" + schedule.children[k].text[starts_with:]
                else:
                    schedule.children[k].text = schedule.children[k].text[starts_with:]

    def update_experience_checked_items(self):
        exp_menu: MenuItem = self.menu
        if exp_menu.cb_tag == 'experience':
            intern = self.info.get('Intern', None)
            jun = self.info.get('Junior', None)
            mid = self.info.get('Middle', None)
            sen = self.info.get('Senior', None)

            for k, v in exp_menu.children.items():
                if exp_menu.children[k].text.find("✅") == -1:
                    starts_with = 0
                else:
                    starts_with = 1

                if self.info.get(k, '') and k.lower() in 'intern junior middle senior':
                    exp_menu.children[k].text = "✅" + exp_menu.children[k].text[starts_with:]
                else:
                    exp_menu.children[k].text = exp_menu.children[k].text[starts_with:]

    def help(self, cb_tag=None):
        cb_tag = self.menu.cb_tag if not cb_tag else cb_tag
        if not cb_tag == 'root':
            help_text = markup_text.help_text.get(cb_tag, markup_text.help_text.get('all_sub_menu', ''))
        else:
            help_text = markup_text.help_text.get(cb_tag, '')

        if help_text:
            result = '\n=====Сообщение с помощью=====\n' if cb_tag != 'start' else ''
            result += help_text
            return result + '\n'

        return ''

    def tags(self):
        """
        #UnrealEngine #GameDev #FullTime #Art #Middle #PC #Remote #Office #ProgramAce

        :return:
        """
        tags = ''
        tags += self.schedule(is_tag=True)
        tags += self.art_code_tag()

        tags += self.jun_mid_sen(is_tag=True)
        tags += self.platform(is_tag=True)

        tags += self.location(is_tag=True)
        tags += self.company(is_tag=True)

        return "#UnrealEngine #GameDev " + tags + '\n\n' if tags else ''

    def art_code_tag(self):
        result = ''
        if self.is_code:
            result += '#Code '
        if self.is_art:
            result += '#Art '

        return result

    def jun_mid_sen(self, is_tag=False, is_title=False):
        intern = self.info.get('Intern', '')
        jun = self.info.get('Junior', '')
        mid = self.info.get('Middle', '')
        sen = self.info.get('Senior', '')

        # print(intern, jun, mid, sen)

        if is_tag:
            pc = f'#{intern} ' if intern else ''
            console = f'#{jun} ' if jun else ''
            vr = f'#{mid} ' if mid else ''
            mobile = f'#{sen} ' if sen else ''
            result = pc + console + vr + mobile

        else:
            to_join = []
            for i in (intern, jun, mid, sen):
                if i:
                    to_join.append(i)
            result = '/'.join(to_join)
            result = f'{result}'
            result = "🧠 " + result + "\n" if result and not is_title else result

        return result if result else ''

    def vacancy_title(self):
        title = self.info.get('vacancy', '')
        title = title.lower().replace('ue5 ', '').replace('ue4 ', '').replace('ue ', '').replace('unreal engine',
                                                                                                 '').replace('unreal ',
                                                                                                             '')
        title = title.replace(' ue5', '').replace(' ue4', '').replace(' ue', '').replace('unreal engine ',
                                                                                         '').replace('unreal',
                                                                                                     '')

        if title:
            title = "UNREAL ENGINE " + title.strip()

        exp = self.jun_mid_sen(is_title=True).upper()
        if exp:
            exp += ' '

        result = exp + title
        result = result.upper()

        company = self.company()
        if company:
            result += f' {company}'
        add_indentation = ''
        if self.project():
            add_indentation = '\n'
        return "<b>" + result + "</b>" + f'\n{add_indentation}' if title or company else ''

    def company(self, is_tag=False):
        company = self.info.get('company', '')

        if is_tag and company:
            return f"#{company.title().replace(' ', '').replace('-', '')} "

        if not is_tag and company:
            company = company.capitalize() if company and company[0].islower() else company
            return f'({company})'
        return ''

    def project(self):
        name = self.info.get('project', '').capitalize()
        platform = self.platform()
        if platform:
            platform = f'{platform}'
        result = ''
        if name or platform:
            name = f' {name} ' if name else ''
            result = '🕹' + name + platform + '\n'

        return result

    def platform(self, is_tag=False):
        pc = self.info.get('PC', None)
        console = self.info.get('Console', None)
        vr = self.info.get('VR/AR', None)
        mobile = self.info.get('Mobile', None)

        if is_tag:
            pc = f'#{pc} ' if pc else ''
            console = f'#{console} ' if console else ''
            vr = f'#VR #AR ' if vr else ''
            mobile = f'#{mobile} ' if mobile else ''
            result = pc + console + vr + mobile

        else:
            to_join = []
            for i in (pc, console, vr, mobile):
                if i:
                    to_join.append(i)
            result = ', '.join(to_join)
            result = f'({result})' if result else ""

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
        result = self.info.get('payment', '')
        return f"💰 {result}\n" if result else ""

    def location(self, is_tag=False):
        remote = self.info.get('Remote', None)
        office = self.info.get('Office', None)
        result = ''
        if is_tag:
            remote = f'#Remote ' if remote else ''
            office = '#Office ' if office else ''
            result = remote + office
        else:
            remote = f'🌎 Удаленно' if remote else ''
            office = f'👔 Офис ({office.title()})' if office else ''

            if remote and office:
                result = f"{remote} || {office}"
            elif remote or office:
                result = remote + office

            if self.info.get('Relocate', ""):
                result += " Relocate\n"
            elif remote or office:
                result += "\n"
            else:
                result += ""

        return result

    def description(self):
        desc = self.info.get('description', '')
        return f'\n🦄 <b>Описание</b>\n{desc}\n' if desc else ''

    def duty(self):
        duty = self.info.get('duty', '')
        return f'\n<b>🚀 Что ты будешь делать</b>{self.to_bullet(duty)}\n' if duty else ''

    def skills(self):
        skills = self.info.get('skills', '')
        return f'\n<b>📚 Твои скиллы</b>{self.to_bullet(skills)}\n' if skills else ''

    def add_skills(self):
        add_skills = self.info.get('add_skills', '')
        return f'\n<b>👍 Круто, если знаешь</b>{self.to_bullet(add_skills)}\n' if add_skills else ''

    def conditions(self):
        cond = self.info.get('conditions', '')
        return f'\n<b>🍪 Условия и плюшки</b>{self.to_bullet(cond)}\n' if cond else ''

    def useful_info(self):
        useful_info = self.info.get('useful_info', '')
        return f'\n<b>ℹ️ Полезная информация</b>\n{useful_info}\n' if useful_info else ''

    def contacts(self):
        contacts = self.info.get('contacts', '')
        return f'\n<b>📨 Контакты</b>\n{contacts}\n' if contacts else ''

    def vacancy_link(self, is_preview=True):
        link = self.info.get('vacancy_link', None)
        if link and is_preview:
            return f"\n🌐 Vacancy link\n"
        elif link:
            return f"\n<a href='{self.info['vacancy_link']}'>🌐 Vacancy link</a>\n"
        else:
            return ''

    @staticmethod
    def to_bullet(text: str, splitter: str = '='):
        list_items = text.splitlines()
        result = ''

        list_items = list(map(str.strip, list_items))
        for item in list_items:
            if item:
                line = item.strip(';.‣•-=— ')
                line = line[0].upper() + line[1:]
                result += '\n• ' + line

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

    def bottom_menu_send_reset(self) -> tuple[InlineKeyboardButton, InlineKeyboardButton]:
        # self.bottom_menu = self.render_menu(BOTTOM_menu)
        # send_button = types.InlineKeyboardButton(BOTTOM_menu['send_vacancy'], callback_data='send_vacancy')
        # reset_button = types.InlineKeyboardButton(BOTTOM_menu['reset_vacancy'], callback_data='reset_vacancy')
        # return (send_button, reset_button)
        pass


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
        if self.cb_tag in MENU_ACTIONS['nothing_exceptions'].split(', '):
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
