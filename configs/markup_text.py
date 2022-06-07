from collections import OrderedDict

USER_MENU = OrderedDict(
    {"company": ("🏢 Компания", {"indie": "Без названия"}),
     "vacancy": ("🖥 Вакансия", {"generalist": "GENERALIST",
                                 "developer": ("DEVELOPER", {"c++_developer": "C++ DEVELOPER",
                                                             "multiplayer_developer": "MULTIPLAYER DEVELOPER",
                                                             "ai_developer": "AI DEVELOPER",
                                                             "gameplay_developer": "GAMEPLAY DEVELOPER"}),
                                 "artist": ('ARTIST', {"3d_artist": "3D ARTIST", "technical_artist": "TECHNICAL ARTIST",
                                                       "environmental_artist": "ENVIRONMENTAL ARTIST",
                                                       "vfx_artist": "VFX ARTIST",
                                                       "lightning_artist": "LIGHTING ARTIST"}),
                                 "designer": (
                                     'DESIGNER',
                                     {"game_designer": "GAME DESIGNER", "motion_designer": "MOTION DESIGNER",
                                      "level_designer": "LEVEL DESIGNER", "ui/ux_designer": "UI/UX DESIGNER"})
                                 }),
     "description": "✍️ Описание",
     "project": ("🕹 Проект", {'PC': 'PC', "Console": 'Console', 'VR/AR': 'VR/AR', "Mobile": 'Mobile'}),
     "experience": (
         "🧠 Опыт",
         {"Intern": "Intern", "Junior": "Junior", "Middle": "Middle", "Senior": "Senior"}),
     "schedule": ("⏰ График", {'Full-Time': "Full-Time", 'Part-Time': "Part-Time", 'Contract': "Contract"}),
     "payment": ("💰 Оплата", {"Negotiable": "По договорённости"}),
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
default_vacancy_name = "generalist, c++_developer, multiplayer_developer, ai_developer,gameplay_developer," \
                                 " 3d_artist,technical_artist, environmental_artist, vfx_artist, lighting_artistgame_designer," \
                                 " motion_designer, level_designer, ui/ux_designer"
MENU_ACTIONS = {
    f"all": "text",
    'nothing_exceptions': "pre_reset_vacancy, root, pre_send_vacancy, Intern, location, Remote, experience, junior, "
                          "senior, middle, Full-Time, Part-Time, Contract, schedule, Relocate, indie, generalist, "
                          "c++_developer, multiplayer_developer, ai_developer,gameplay_developer, 3d_artist,"
                          " technical_artist, environmental_artist, vfx_artist, lighting_artist"
                          "game_designer, motion_designer, level_designer, ui/ux_designer",

    "not_clear": "payment, root, pre_send_vacancy, schedule, pre_reset_vacancy, send_verif, reset_verif"
}

MP_WIDTH = {
    "all": 3,
    "experience": 4,
    "project": 4,
    "vacancy": 2,
    'designer': 2,
    'developer': 2,
    'artist': 2
}

help_text = {
    # сообщение по дефолту для каждого подменю
    'all_sub_menu': '',

    # start только в руте будет и когда нет данных
    'start': "Добро пожаловать, {name}! Бот поможет опубликовать вакансию на канале @uejobs. В этом сообщении вы увидите предпросмотр вашей вакансии, когда начнёте заполнять информацию",

    # 'root': '',
    'company': "Enter Company Name",
    'vacancy': "Enter Vacancy title",
    'description': "Enter Description",
    'project': "Enter the Name of your project",
    'experience': "What candidate do you want",
    'schedule': "How are you working?",
    'payment': "Выберите \"По договоренности\" или введите свое значение",
    'location': "Where do you place?",
    'duty': "",
    'skills': "",
    'add_skills': "",
    'conditions': "What do you offer?",
    'useful_info': "Do you have useful information?",
    'contacts': "How contact you?",
    'pre_reset_vacancy': "",

}
AFTER_SEND_MP = (('🔥Опубликовать новую вакансию🔥', '/new'), ('Вернуться в меню', "back_menu"))
AFTER_SEND_ALERT = '📬Вакансия отправлена на модерацию!📬'

ART_PATTERN = "artist, художник, animator, art, Designer, Generalist".lower().split(', ')
CODE_PATTERN = "developer, разработчик, programmer, программист, dev, ENGINEER, TECHNICAL".lower().split(', ')
CHAR_CLEAN = ';.‣•-=—*· ●–⁃✔️◦ '
