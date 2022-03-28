from collections import OrderedDict

# отсюда создается STAGES при init в Vacancy
# STAGES = {0:"vacancy_title"}
"""
'---' сопоставимо с None, Unknown...

"""
USER_MENU = OrderedDict(
    {"company": "🏢 Компания",
     "vacancy": "🖥 Вакансия",
     "description": "✍️ Описание",
     "project": ("🕹 Проект", {'PC': 'PC', "Console": 'Console', 'VR/AR': 'VR/AR', "Mobile": 'Mobile'}),
     "sub_experince": (
         "🧠 Опыт",
         {"Intern": "INTERN", "Junior": "JUNIOR", "Middle": "MIDDLE", "Senior": "SENIOR"}),
     "schedule": ("⏰ График", {'Full-Time': "Full-Time", 'Part-Time': "Part-Time", 'Contract': "Contract"}),
     "payment": ("💰 Оплата", {"Negotiable": "По договоренности"}),
     "location": ("🗺 Локация", {'Remote': 'Remote', "Office": "Office", "Relocate": "Relocate"}),
     "duty": "🚀 Обязанности",
     "skills": "💪 Скилл сет",
     "add_skills": "🦾 Доп. скиллы",
     "conditions": "🍪 Условия",
     "useful_info": "ℹ️ Доп.инфо",
     "contacts": "📨 Контакты",
     "vacancy_link": "🌐 Vacancy link",

     # {"callback_tag": ("menu_text",
     #                  {'submenu_tag': ("submenu_text",
     #                                   {"sub_submenu": "sub_submenu_text"})}),
     #  }
     })
# text, auto_input, inline_input
MENU_ACTIONS = {
    f"all": "text",
    'nothing_exceptions': "root, Intern, location, Remote, sub_experince, junior, senior, middle, Full-Time, "
                          "Part-Time, Contract schedule Relocate",
    "not_clear": "payment project"
}

MP_WIDTH = {
    "all": 3,
    "sub_experince": 4,
    "project": 4
}
# todo
BOTTOM_menu = {"reset": "❌ Сброс", "send_vacancy": "Отправить на публикацию"}
