import mysql.connector
#кофиг конекта
dbconfig = {'host': 'host',
            'user': 'admin',
            'password': 'adminpwd',
            'database': 'blogdb',}

# класс конекта к БД
# перегружаем для работы с менеджером контекста
class UseDatabase:
    def __init__(self, config:dict, subd=mysql.connector) -> None:
        self.configuration = config
        self.subd = subd

    def __enter__(self) -> 'cursor':        
        self.conn = self.subd.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, ext_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

# конектимся к бд, учитывая, что запрос может ничего  не возвратить(update / insert)
def get_request(SQL, dbconfig, *args:None):
    try:
        with UseDatabase(dbconfig) as cursor:
            if args:
                cursor.execute(SQL, args)
            else:
                cursor.execute(SQL)
            r = cursor.fetchall()
    except mysql.connector.errors.InterfaceError:
        return 'InterfaceError or empty fetch'
    return  r