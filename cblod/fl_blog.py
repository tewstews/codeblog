from flask import *
from dbcn import get_request 
from user_function import *
from SQL.sql_scripts import *
import cgi
import random
import math

# dbcn.get_request(запрос_из_модуля_get_reques], файл_конфига, *аргументы_для_форматирования_запроса])

app = Flask(__name__)
app.secret_key = 'key'
app.config['STATIC_FOLDER'] = 'static'


# Авторизация 
@app.route('/', methods=['GET', 'POST'])
@check_authorized
def enter() -> 'html':

    if request.method == 'GET':
        is_authorized = False
    elif request.method == 'POST':
        login = request.form['login'].lower()
        pwd = request.form['pwd']
        # форматируем запрос
        qry = user_exists % (login, pwd)
        # если вовращается фетч, значит юзер существует, адресуем на user_page_pagination
        # в противном случае записываем в переменную авториазции False
        fetch = get_request(qry, dbconfig)
        
        if fetch:
            session['user'] = login
            return redirect(url_for('user_page_pagination', user = session['user'], page = 1))
        else:
            is_authorized = False

    return render_template( 'enter.html', 
                            template_folder='templates', 
                            title='AUTH_PAGE', 
                            not_find_user = True \
                                                  if request.method == 'POST' and is_authorized == False \
                                                  else False)


# ------ пересмотреть логику регистрации, есть неочевидные момемнты
# Регистрация 
@app.route('/regist/', methods=['GET', 'POST'])
@check_authorized
def app_register() -> 'html':
    # принмиаем, что при любом  GET запросе регистрация не может быть проведена, 
    # по этому опрашиваем форму только при POST
    if request.method == 'GET':
        is_exists_auth_data = False
    elif request.method == 'POST':        
        login = request.form['login'].lower()
        pwd = request.form['pwd']
        mail = request.form['mail']
        # присваиваем рандомный аватар
        avatars_list = get_file_list(app.static_folder, 'images/user_avatars/')
        avatars_image =  '/static/images/user_avatars/' + random.choice(avatars_list)
        # проверка на существование юзера
        try:
            get_request(users_insert, dbconfig, login, mail, pwd, avatars_image)
        except mysql.connector.errors.IntegrityError as err:
            is_exists_auth_data = True

    return render_template( 'regist.html', 
                            template_folder='templates',
                            title='AUTH_PAGE',
                            fail = True if is_exists_auth_data else False)      


# страница пользователя
@check_logged_in
@app.route('/<user>/<int:page>', strict_slashes=False, methods=['GET',])
def user_page_pagination(user, page):
    # храним номер запрашиваемой страницы и текущий роут для возврата после аресации
    # на служебные роуты
    session['current_page'] = int(page)
    session['current_route'] = 'user_page'

    # проверка на соответвие запрашивоемой странице аторизованного юзера
    if user != session['user']:
        return redirect(url_for('user_page_pagination', user=session['user'], page=1))

    # переменные для пагинации
    # вычисляем стартовую и конечную позицию на основании кол-ва постов в роуте
    cnt_post =  get_request(select_cnt_posts, dbconfig, session['user'])[0][0]    
    # постов на страницу
    post_to_page   = 5
    position_start = post_to_page*(int(page) - 1)
    position_end   = post_to_page
    pages_cnt      = int(math.ceil(cnt_post / post_to_page))    
    # отображаемое кол-во роутов на страницу
    cnt_pagi_pages = 10
    current_pagi_state = session['current_page'] * post_to_page
    # генерим список страниц пагинации
    pagination_list = [i for i in range(1, pages_cnt+1)]
    pagination_list = pagination_list[session['current_page']-1:cnt_pagi_pages+session['current_page']-1]
    # получаем нужное кол-во постов
    posts = get_request(select_posts_user, dbconfig, user, position_start, position_end)
    session['current_page'] = page 

    return render_template('user_page.html',
                           template_folder='templates', 
                           title='USER_PAGE',
                           user_name=session['user'], 
                           posts = posts, 
                           cnt_p = cnt_post, 
                           pages = pages_cnt-1, 
                           pagination_urls='',
                           pagination_list=pagination_list,)


# создаем посты
@check_logged_in
@app.route('/create_post', methods=['POST',])
def create_post():
    # храним номер запрашиваемой страницы для возврата после аресации
    # на служебные роуты
    user = session['user']
    post_tags    = request.form['tags']
    form_content = request.form['post_create']
    #опрашиваем чекбокс настроек приватности поста
    is_private = 'PRV' if 'is_private' in request.form else 'PUB'

    get_request(insert_post, dbconfig, user, form_content, post_tags, is_private)

    return redirect('/' + user + '/' + str(session['current_page']))

# тестовый роут 
@app.route('/test_session/')
def test_session():
    #session['current_page'] = 1
    #sessison_types = {type(v) for v in session.values()}
    return str(app.static_folder)

# удаление постов
@check_logged_in
@app.route('/delete_post/<post_id>', methods=['GET',])
def delete_post_route(post_id):
    
    post_to_del = int(post_id)
    # удалить пост пользователя может только автор поста
    user = session['user']
    get_request(delete_post, dbconfig, user, post_to_del)

    return redirect('/' + user + '/' + str(session['current_page']))

# --- добавить поиск по тегам
# --- лента
@check_logged_in
@app.route('/explore/<page>', methods=['GET',])
def explore(page):    
    # храним номер запрашиваемой страницы, поисковый запрос, текущий роут в сессии
    session['current_page'] = int(page)
    session['search_request'] = exp_request = request.args.get('req') 
    session['current_route'] = 'explore'
    # пагинация для ленты
    post_to_page   = 5
    position_start = post_to_page*(int(page) - 1) 
    position_end   = post_to_page

    # -----перенести логику пагинации в отдельный модуль -------
    # кол-во постов для пагинаии
    if exp_request:
        cnt_post = get_request(select_cnt_posts_explore.format(exp_request), dbconfig)[0][0]
        pagination_urls =  '?' + 'req=' + exp_request
    else:
        cnt_post = get_request(select_cnt_posts_all, dbconfig)[0][0]
        pagination_urls = ''
    
    pages_cnt = int(math.ceil(cnt_post / post_to_page)) 

    # если постов больше, чем преполагается для вызова пагинции, отображать пагинацию
    # иначе выводить все
    if pages_cnt > 10:
        cnt_pagi_pages = 10
        current_pagi_state = session['current_page'] * post_to_page
        pagination_list = [i for i in range(1, pages_cnt+1)]
        pagination_list = pagination_list[session['current_page']-1:cnt_pagi_pages+session['current_page']-1]
    else:
        pagination_list =  [i for i in range(1, pages_cnt+1)]

    # в случае наличия поисквого  запроса, выводить посты согласно поискового запроса
    if exp_request:   
        get_select_explore = select_explore.format(exp_request, position_start, position_end)
    else:
        get_select_explore = select_explore_all.format(position_start, position_end)
    
    posts = get_request(get_select_explore, dbconfig)

    return render_template('user_page.html', 
                            template_folder='templates', 
                            title='Explore',
                            user_name=session['user'],
                            posts = posts,
                            cnt_p = cnt_post,
                            pages = pages_cnt-1,
                            pagination_urls=pagination_urls,
                            pagination_list=pagination_list)


# инфо о юзере
@check_logged_in
@app.route('/<user>/profile/')
def profile(user):
    user_profile  = user
    user_info = get_request(select_user_info, dbconfig, user_profile)
    
    return render_template('profile.html', tittle='Profile', user_info = user_info)



@app.route('/logout/')
def logout():
    session.pop('user')
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)