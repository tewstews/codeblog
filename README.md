# codeblog
 blog for code exchange

Реализованно:
- регистрация
- авторизация
- пагинация
- поиск
- лента
- страница пользователя
- создание и удаление постоав

Планируется:
- чат
- подписики
- рейтинг
- редактирование инфо


структура:
- fl_blog.py - главной модуль, роуты, логика генерации шаблонов
- user_function.py - функции вне сторонних модулей
- dbcn.py - модуль конекта к бд
- /templates/ - html(jinja2) шаблоны
- /SQL/creating_tables.sql - шаблон таблиц
- /SQL/sql_scripts.py - sql звпросы в виде переменных
- /static/ - -js, html, css
