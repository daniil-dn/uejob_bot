from collections import OrderedDict

# отсюда создается STAGES при init в Vacancy
# STAGES = {0:"vacancy_title"}
"""
'---' сопоставимо с None, Unknown...

"""
WHERE_SEND = '-621961119'

USER_MENU = OrderedDict(
    {"company": "🏢 Компания",
     "vacancy": "🖥 Вакансия",
     "description": "✍️ Описание",
     "project": ("🕹 Проект", {'PC': 'PC', "Console": 'Console', 'VR/AR': 'VR/AR', "Mobile": 'Mobile'}),
     "experience": (
         "🧠 Опыт",
         {"Intern": "Intern", "Junior": "Junior", "Middle": "Middle", "Senior": "Senior"}),
     "schedule": ("⏰ График", {'Full-Time': "Full-Time", 'Part-Time': "Part-Time", 'Contract': "Contract"}),
     "payment": ("💰 Оплата", {"Negotiable": "По договоренности"}),
     "location": ("🗺 Локация", {'Remote': 'Remote', "Office": "Office", "Relocate": "Relocate"}),
     "duty": "🚀 Обязанности",
     "skills": "💪 Скилл сет",
     "add_skills": "🦾 Доп. скиллы",
     "conditions": "🍪 Условия",
     "useful_info": "ℹ️ Полезная информация",
     "contacts": ("📨 Контакты", {"vacancy_link": "🌐 Vacancy link"}),

     "pre_send_vacancy": ("✅ Опубликовать", {"send_verif": "✅ Опубликовать"}),
     "pre_reset_vacancy": ("❌ Сброс", {"reset_verif": "❌ Сброс"})

     # {"callback_tag": ("menu_text",
     #                  {'submenu_tag': ("submenu_text",
     #                                   {"sub_submenu": "sub_submenu_text"})}),
     #  }
     })
# text, auto_input, inline_input
MENU_ACTIONS = {
    f"all": "text",
    'nothing_exceptions': "pre_reset_vacancy, root, pre_send_vacancy, Intern, location, Remote, experience, junior, senior, middle, Full-Time, Part-Time, Contract, schedule, Relocate",
    "not_clear": "payment, root, pre_send_vacancy, schedule, pre_reset_vacancy, send_verif, reset_verif"
}

MP_WIDTH = {
    "all": 3,
    "experience": 4,
    "project": 4
}

help_text = {
    # сообщение по дефолту для каждого подменю
    'all_sub_menu': '',

    # start только в руте будет и когда нет данных
    'start': "Добро пожаловать, {name}! Бот поможет опубликовать вакансию на канале @uejobs. В этом сообщении вы увидите предпросмотр вашей вакансии, когда начнёте заполнять информацию\n",

    # 'root': '',
    'company': "",
    'vacancy': "",
    'description': "",
    'project': "",
    'experience': "",
    'schedule': "",
    'payment': "Выберите \"По договоренности\" или введите свое значение",
    'location': "",
    'duty': "",
    'skills': "",
    'add_skills': "",
    'conditions': "",
    'useful_info': "",
    'contacts': "",
    'pre_reset_vacancy': "",

}
AFTER_SEND_MP = (('🔥Опубликовать новую вакансию🔥', '/new'), ('Вернуться в меню', "back_menu"))
AFTER_SEND_ALERT = '📬Вакансия отправлена на модерацию!📬'

ART_PATTERN = "artist, художник, animator, art, Designer, Generalist".lower().split(', ')
CODE_PATTERN = "developer, разработчик, programmer, программист, dev, ENGINEER, TECHNICAL".lower().split(', ')
