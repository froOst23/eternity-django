"""
data

Переменная, которая хранит в себе название сайта, 
название и ссылки для header, footer
"""
data = {
    'site_title': 'eternity',
    'header_nav': [
        {'item': 'Главное меню', 'url': '/'},
        {'item': 'Связь', 'url': '/about'},
        {'item': 'Сделать пост', 'url': '/add_post'}
    ],
    'header_auth': [
        {'item': 'Вход', 'url': '/'},
        {'item': 'Регистрация', 'url': '/'}
    ],
    'footer': [
        {'item': '© eternity 2020', 'url': '/'}
    ]
}
