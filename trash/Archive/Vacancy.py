import re
from collections import OrderedDict

from aiogram import types

vacancy_per_user = {}


class Vacancy:
    # ToDo инициализировать словарь шагов из массива текста для клавиатуры
    def __init__(self):
        self.stage = 0

        #создает из text_pattern словарь:
        #     'vacancy_title'
        self.STAGES = []
        for i in self.text_pattern.keys():
            self.STAGES.append(i)


    def __str__(self):
        return self.info

    text_pattern = OrderedDict({
        "vacancy_title": ("Название вакансии👇",
            ('UNREAL ENGINE C++ DEVELOPER', 'UNREAL ENGINE DEVELOPER', 'GAME DESIGNER', '3D ARTIST')),
        "skill_level": ("Уровень Skill👇", ('junior', 'middle', 'senior')),
        "company_name": ("Название компании👇", ("None",)),
        "game_title": ("Название игры👇", ("Unknown",)),
        "art_code": ("art / code", ('art', 'code')),
        "years": ("Сколько лет опыта👇", ("None", 1, 2, 3, 4, 5)),
        "platform": ("Платформа👇", (
            'PC, Console', 'PC', 'PC, VR', 'PC, Mobile', 'PC, Mobile, Console', 'PC, Mobile, Console, VR',
            'PC, Console, VR',
            'Mobile',
            'Console', 'VR')),
        "remote": ("Удаленка?👇", ("None", 'Remote')),
        "office": ("Офис есть? Или не написан город?👇", ("None", "не написан город", "Москва", "Санкт-Петербург", "Киев")),
        "money": ("💰 ?👇", ('По договоренности',)),
        "schedule": ("Какой график работы?", ('Full-time', 'Part-time', 'Contract')),
        "description": ("Описание компании", ('None',)),
        "resp": ("Что ты будешь делать '=' - разделитель", ('None',)),
        "require": ("Твои скиллы '=' - разделитель", ('None',)),
        "plus": ("Круто, если знаешь '=' - разделитель", ('None',)),
        "cond": ("Условия и плюшки '=' - разделитель", ('None',)),
        "useful": (" Полезная информация '=' - разделитель", ('None',)),
        "contacts": ("Контакты", ('Ingamejob', 'Djinni', "Head Hunter")),
    })

    # Массив введенной информации
    info = {
    }

    # Создает клавиатуру для каждого шага
    # todo refactoring
    def get_markup(self):
        markup = types.ReplyKeyboardMarkup(row_width=len(self.text_pattern[self.stage][1]))

        for i in range(len(self.text_pattern[self.stage][1])):
            item = types.KeyboardButton(self.text_pattern[self.stage][1][i])
            markup.add(item)
        return markup

    # текст для каждого шага - используется только в команде /new /start
    def get_text_per_stage(self):
        return self.text_pattern[self.STAGES[self.stage]][0]

    def get_tag_office_remote(self) -> tuple:
        # todo refactoring
        result = ''
        is_remote = True
        is_office = True

        # город
        office_place = None

        # Если находит none в шаге remote
        if self.info["remote"].lower().find('none') != -1:
            is_remote = False
        else:
            result = '#Remote'

        # Если находит none в шаге office
        if self.info["office"].lower().find('none') != -1:
            is_office = False
        else:
            office_place = self.info[self.STAGES[8]]
            if office_place[0].islower():
                office_place = office_place.title()
            if is_remote:
                result += ' '
            result += '#Office'
        return result, office_place

    # todo поправить регистры в тегах - заметил пока только в название компании прыгает кейс
    def get_tags(self):
        platforms = ''
        for item in self.info[self.STAGES[6]].split(','):
            platforms += f'#{item.strip()} '

        # todo вывод название компании через функцию get_company_name()
        company = ''
        if self.info['company_name'].lower().find('none') != -1:
            company = 'indie'
        else:
            company = self.info['company_name'].strip().title()
            company = company.replace(' ', '')

        full_part_contract = 'FullTime'
        match self.info['schedule'].strip().lower():
            # 'Full-time', 'Part-time', 'Contract'
            case 'full-time':
                full_part_contract = 'FullTime'
            case 'part-time':
                full_part_contract = 'PartTime'
            case 'contract':
                full_part_contract = 'Contract'

        return f'#UnrealEngine #GameDev #{full_part_contract} #{self.info[self.STAGES[4]].capitalize()} #{self.info["skill_level"].capitalize()} {self.get_platforms(is_tags=True)} {self.get_tag_office_remote()[0]} #{company.capitalize()}'

    # Название вакансии всегда в UPPER CASE
    def get_vacancy_title(self):
        return self.info['vacancy_title'].strip().upper()

    # название комании
    def get_company_name(self, is_tag=False):
        if self.info['company_name'].lower().find('none') != -1:
            return ''
        else:
            return f"({self.info['company_name'].title() if self.info['company_name'].islower() else self.info['company_name']})"

    # лет опыта
    def get_years(self):
        if self.info['years'].lower().find('none') == -1 and self.info['years'].lower().isdigit():
            return f"({self.info['years']}+)"
        else:
            return ''

    # место работы - удаленно, офис
    # todo refactoring
    def get_location(self):

        result = ''
        remote_str = ''
        office_str = ''
        office_remote_tuple = []
        office_place = None
        if self.info['remote'].lower().find('none') == -1:
            remote_str = '🌎 Удаленно'
            office_remote_tuple.append(remote_str)
        if self.info['office'].lower().find('none') == -1:
            office_str = '👔 Офис'
            if self.info['office'].find("Не написан город") == -1:
                office_str += f"({self.info['office'].title() if self.info['office'][0].islower else self.info['office']})"
            office_remote_tuple.append(office_str)
        return ' || '.join(office_remote_tuple)

    # Платформа работы
    # todo refactoring
    def get_platforms(self, is_tags=False):
        result = []
        for i in self.info['platform'].split(","):
            i = i.strip()
            # для платформ, которые обычно пишутся как сокращения
            # todo refactoring
            if len(i) < 4 or i in ('VR/AR'):
                if is_tags:
                    result.append('#' + i.upper())
                else:
                    result.append(i.upper())
            else:
                if is_tags:
                    result.append('#' + i.title())
                else:
                    result.append(i.title())

        return ' '.join(result) if is_tags else ', '.join(result)

    # парсит по шаблону текст в список. Разбивая по "="
    # todo refactoring
    def get_bullet_text(self, info_key):
        template_bullet = {
            'description': '🦄 ',
            'resp': '🚀 Что ты будешь делать',
            'require': '📚 Твои скиллы',
            'plus': '👍 Круто, если знаешь',
            'cond': '🍪 Условия и плюшки',
            'useful': 'ℹ️ Полезная информация'
        }
        if self.info[info_key].lower().find('none') != -1:
            return ''

        result = ''
        result += f"<b>{template_bullet[info_key]}</b>"
        if info_key == 'description':
            return result + self.info[info_key] + '\n\n'

        list_items = self.info[info_key].split('=')

        list_items = list(map(str.strip, list_items))
        for item in list_items:
            if item:
                result += '\n• ' + item.replace(';', '')
        result += '\n\n'

        return result

    # todo сделать парсинг контактов
    def get_contacts(self):
        resource_name_exp = r'^((?!-)[A-Za-z0-9-]{1, 63}(?<!-)\\.)+[A-Za-z]{2, 6}$'
        result = '📨 Контакты \n'
        return result + self.info['contacts']

    # итоговая вакансия
    def get_ready_vacancy(self):
        result = f"""
{self.get_tags()}\n
<b>{self.info['skill_level'].upper()} {self.get_vacancy_title()} {self.get_company_name()}</b>

🕹 {self.info['game_title'].title()} ({self.get_platforms()})
🧠 {self.info['skill_level'].title()} {self.get_years()}
💰 {self.info['money'].capitalize()}
⏰ {self.info['schedule'].title()}
    """
        result += f"{self.get_location()}\n\n"
        result += f"{self.get_bullet_text('description')}"
        result += f"{self.get_bullet_text('resp')}"
        result += f"{self.get_bullet_text('require')}"
        result += f"{self.get_bullet_text('plus')}"
        result += f"{self.get_bullet_text('cond')}"
        result += f"{self.get_bullet_text('useful')}"
        result += f"{self.get_contacts()}\nВакансия на"
        return result
