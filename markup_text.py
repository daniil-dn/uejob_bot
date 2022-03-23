from collections import OrderedDict

# отсюда создается STAGES при init в Vacancy
# STAGES = {0:"vacancy_title"}
"""
'---' сопоставимо с None, Unknown...

"""
COMMANDS = ("menu", "show_vacancy", "start_over", "continue_filling")
text_pattern = OrderedDict({
    "company_name": ("👇 Название компании 👇", ("indie",)),
    "vacancy_title": ("👇 Название вакансии 👇",
                      ('UNREAL ENGINE C++ DEVELOPER', 'UNREAL ENGINE DEVELOPER', 'GAME DESIGNER', '3D ARTIST')),
    "art_code": ("Art 👨‍🎨 || Сode 🧑‍💻", ('art', 'code')),
    "skill_level": ("👇 Уровень Skill 👇", ('Junior', 'Middle', 'Senior')),
    "game_title": ("🕹 Название игры 🕹", ("Unknown",)),
    "years": ("🧠 Сколько лет опыта 🧠", ("---", 1, 2, 3, 4, 5)),
    "platform": ("🎛 Платформа 🎛", (
        'PC, Console', 'PC', 'PC, VR', 'PC, Mobile', 'PC, Mobile, Console', 'PC, Mobile, Console, VR',
        'PC, Console, VR',
        'Mobile',
        'Console', 'VR')),
    "remote": ("🌎  Удаленка? 🌎 ", ("---", 'Remote')),
    "office": ("💼 Офис есть? 💼", ("---", "Москва", "Санкт-Петербург", "Киев", "Екатеринбург", "Омск")),
    "money": ("💰 Что по $$$ ? 💰", ('По договоренности',)),
    "schedule": ("⏰ Какой график работы? ⏰", ('Full-time', 'Part-time', 'Contract')),
    "description": ("🦄 Описание", ('---',)),
    "resp": ("🚀  Что ты будешь делать 🚀\n '=' - разделитель", ('---',)),
    "require": ("📚 Твои скиллы 📚\n '=' - разделитель", ('---',)),
    "plus": ("👍 Круто, если знаешь 👍\n '=' - разделитель", ('---',)),
    "cond": ("🍪 Условия и плюшки 🍪\n '=' - разделитель", ('---',)),
    "useful": ("ℹ️  Полезная информация ℹ️\n'=' - разделитель", ('---',)),
    "contacts": ("📨 Контакты 📨", ('---',)),

})
# {"tags": (
# cb.data,
# {tags:cb.data,tags:cb.data,..})
# }

USER_MENU = OrderedDict(
    {"company": "🏢 Компания",
     "vacancy": "🖥 Вакансия",
     "art_code": ("Art или Code", {'art': 'art', 'code': "code"}),
     "description": "✍️ Описание",
     "project": "🕹 Проект",
     "platform": ("🎮 Платформа", {'PC': 'PC', "Console": 'Console', 'VR': 'VR', "Mobile": 'Mobile'}),
     "sub_experince": (
         "🧠 Опыт",
         {'years': 'Years', "Junior": "Junior <1year", "Middle": "Middle 1-3years", "Senior": "Senior >3years"}),
     "schedule": ("⏰ Загрузка", {'Full-Time': "Full-Time", 'Part-Time': "Part-Time", 'Contract': "Contract"}),
     "payment": "💰 Оплата",
     "location": ("🗺 Локация", {'Remote': 'Remote', "Office": "Office -> Город"}),
     "duty": "🚀 Обязанности",
     "skills": "💪 Скилл сет",
     "add_skills": "🦾 Доп. скиллы",
     "conditions": "🍪 Условия",
     "useful_info": "ℹ️ Полезная информация",
     "contacts": "📨 Контакты",

     # {"callback_tag": ("menu_text",
     #                  {'submenu_tag': ("submenu_text",
     #                                   {"sub_submenu": "sub_submenu_text"})}),
     #  }
     })
# text, auto_input, inline_input
MENU_ACTIONS = {
    f"all": "text",
    'nothing_exceptions': "root, location,Remote, sub_experince, junior, senior, middle, Full-Time, Part-Time, Contract"
}

MP_WIDTH = {
    "all": 3,
    "sub_experince": 4,
    "platform": 4
}
# todo
BOTTOM_menu = {"send_vacancy": "✅ Опубликовать", "reset": "❌ Сброс"}
