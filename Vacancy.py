import re

from aiogram import types

vacancy_per_user = {}


class Vacancy:
    def __init__(self):
        self.stage = 0

    def __str__(self):
        return self.info

    STAGES = {
        0: "vacancy_title",
        1: "skill_level",
        2: "company_name",
        3: "game_title",
        4: 'art_code',
        5: 'years',
        6: "platform",
        7: 'remote',
        8: "office",
        9: 'money',
        10: 'schedule',
        11: 'description',
        12: 'resp',
        13: 'require',
        14: "plus",
        15: "cond",
        16: 'useful',
        17: 'contacts',
    }
    text_pattern = {
        0: ("Название вакансии👇",
            ('UNREAL ENGINE C++ DEVELOPER', 'UNREAL ENGINE DEVELOPER', 'GAME DESIGNER', '3D ARTIST')),
        1: ("Уровень Skill👇", ('junior', 'middle', 'senior')),
        2: ("Название компании👇", ("None",)),
        3: ("Название игры👇", ("Unknown",)),
        4: ("art / code", ('art', 'code')),
        5: ("Сколько лет опыта👇", ("None", 1, 2, 3, 4, 5)),
        6: ("Платформа👇", (
            'PC, Console', 'PC', 'PC, Mobile', 'PC, Mobile, Console', 'PC, Mobile, Console, VR', 'PC, Console, VR',
            'Mobile',
            'Console', 'VR')),
        7: ("Удаленка?👇", ("None", 'remote')),
        8: ("Офис есть? Или не написан город?👇", ("None", "не написан город", "Москва", "Санкт-Петербург", "Киев")),
        9: ("💰 ?👇", ('По договоренности',)),
        10: ("Какой график работы?", ('Full-time', 'Part-time')),
        11: ("Описание компании  '-' - разделитель", ('None',)),
        12: ("Что ты будешь делать '-' - разделитель", ('None',)),
        13: ("Твои скиллы '-' - разделитель", ('None',)),
        14: ("Круто, если знаешь '-' - разделитель", ('None',)),
        15: ("Условия и плюшки '-' - разделитель", ('None',)),
        16: (" Полезная информация '-' - разделитель", ('None',)),
        17: ("Контакты", ('Ingamejob', 'Djinni', "Head Hunter")),
    }
    info = {
    }

    def get_markup(self):
        markup = types.ReplyKeyboardMarkup(row_width=len(self.text_pattern[self.stage][1]))
        for i in range(len(self.text_pattern[self.stage][1])):
            item = types.KeyboardButton(self.text_pattern[self.stage][1][i])
            markup.add(item)
        return markup

    def get_text(self):
        return self.text_pattern[self.stage][0]

    def get_office_remote(self) -> tuple:
        result = ''
        is_remote = True
        is_office = True
        office_place = None
        if self.info[self.STAGES[7]].lower().find('none') != -1:
            is_remote = False
        else:
            result = '#remote '
        if self.info[self.STAGES[8]].lower().find('none') != -1:
            is_office = False
        else:
            office_place = self.info[self.STAGES[8]].title()
            result += '#office'
        return result, office_place

    def get_tags(self):
        platforms = ''
        for item in self.info[self.STAGES[6]].split(','):
            platforms += f'#{item.strip()} '
        company = ''
        if self.info['company_name'].find('none') != -1:
            company = 'indie'
        else:
            company = self.info['company_name'].strip().title()
            company = company.replace(' ', '')
        return f'#unrealengine #gamedev #{self.info[self.STAGES[4]]} #{self.info[self.STAGES[1]]} {platforms} {self.get_office_remote()[0]} #{company}'

    def get_vacancy_title(self):
        return self.info['vacancy_title'].strip().upper()

    def get_company_name(self):
        if self.info['company_name'].find('none') != -1:
            return ''
        else:
            return f"({self.info['company_name'].title()})"

    def get_years(self):
        if self.info['years'].find('none') == -1 and self.info['years'].isdigit():
            return f"({self.info['years']}+)"
        else:
            return ''

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
            if self.info['office'].find("не написан город") == -1:
                office_str += f" ({self.info['office'].title()})"
            office_remote_tuple.append(office_str)
        return ' || '.join(office_remote_tuple)

    def get_platforms(self):
        result = []
        for i in self.info['platform'].split(","):
            i = i.strip()
            if len(i) < 4 or i in ('vr/ar'):
                result.append(i.upper())
            else:
                result.append(i.title())
        return ', '.join(result)

    def get_bullet_text(self, info_key):
        template_bullet = {
            'description': '🦄',
            'resp': '🚀 Что ты будешь делать',
            'require': '📚 Твои скиллы',
            'plus': '👍 Круто, если знаешь',
            'cond': '🍪 Условия и плюшки',
            'useful': 'ℹ️ Полезная информация',
            'contacts': '📨 Контакты',
        }
        if self.info[info_key].find('none') != -1:
            return ''

        result = ''
        result += f"<b>{template_bullet[info_key]}</b>"
        if info_key == 'description':
            return result + self.info[info_key].capitalize() + '\n\n'

        list_items = self.info[info_key].split('-')

        list_items = list(map(str.strip, list_items))
        for item in list_items:
            if item:
                result += '\n• ' + item.capitalize()
        result += '\n\n'
        return result

    def get_contacts(self):
        resource_name_exp = r'^((?!-)[A-Za-z0-9-]{1, 63}(?<!-)\\.)+[A-Za-z]{2, 6}$'
        return self.info['contacts']

    def get_ready_vacancy(self):
        result = f"""
{self.get_tags()}\n
<b>{self.info['skill_level'].upper()} {self.get_vacancy_title()} {self.get_company_name()}</b>
🕹{self.info['game_title'].title()} ({self.get_platforms()})
🧠{self.info['skill_level'].title()} {self.get_years()}
💰{self.info['money'].lower()}
⏰{self.info['schedule'].title()}
"""
        result += f"{self.get_location()}\n\n"
        result += f"{self.get_bullet_text('description')}"
        result += f"{self.get_bullet_text('resp')}"
        result += f"{self.get_bullet_text('require')}"
        result += f"{self.get_bullet_text('plus')}"
        result += f"{self.get_bullet_text('cond')}"
        result += f"{self.get_bullet_text('useful')}"
        result += f"{self.get_contacts()}\nВакансия на"
        result += f"  "

        return result
