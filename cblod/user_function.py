from flask import *
from functools import wraps
from dbcn import *
from SQL.sql_scripts import *
import os

# проверяем залогинен ли юзер для доступа к страницам
def check_logged_in(func) -> str:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            if session['user'] == kwargs['user']:
                return func(*args, **kwargs)
        else:
            return redirect(url_for('enter'))
    return wrapper

# проверяем залогинен ли юзер для возврата на главную
def check_authorized(func) -> str:
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not 'user' in session:
            return func(*args, **kwargs)
        elif 'user' in session:
            return redirect(url_for('user_page_pagination',  user=session['user'], page='1'))
    return wrapped

# получаем содержимое папки
def get_file_list(folder_static:str, folder_to_join:str)-> list:
    a = os.listdir(os.path.join(folder_static , folder_to_join))
    return a