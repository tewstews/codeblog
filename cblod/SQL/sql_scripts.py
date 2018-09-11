users_insert = """insert into users
                      (USER_LOGIN, USER_EMAIL, USER_PWD, AVATARS_PATH)
                      values 
                      (%s, %s, %s, %s);"""

                      
user_exists  = """select 1 from users where USER_LOGIN = '%s' and USER_PWD = '%s';""" 


insert_post = """insert into USER_POSTS (
                      USER_LOGIN, POST_CONTENT, POST_TAGS, POST_STATE)
                      values 
                      (%s, %s, %s, %s);"""

select_posts_user = """select POST_CONTENT,  POST_TAGS, POST_ID, USER_LOGIN, POST_DATE
                         from USER_POSTS 
                        where USER_LOGIN = %s 
                        order by POST_DATE desc
                        limit %s, %s;"""

select_cnt_posts = """select count(distinct POST_ID) 
                        from USER_POSTS
                       where USER_LOGIN = %s;"""

select_cnt_posts_all = """select count(distinct POST_ID) 
                        from USER_POSTS
                       where POST_STATE = 'PUB';"""

select_cnt_posts_explore =  """select count(distinct POST_ID) 
                        from USER_POSTS 
                       where (POST_TAGS = '{0}'
                          or POST_ID  = '{0}'
                          or POST_CONTENT like '%{0}%'
                          or USER_LOGIN  = '{0}'
                          or year(POST_DATE) = '{0}'
                          or month(POST_DATE) = '{0}'
                          or day(POST_DATE) = '{0}'
                          or date(POST_DATE) = '{0}')
                         and POST_STATE = 'PUB'"""                                             

delete_post = """delete USER_POSTS from USER_POSTS where USER_LOGIN = %s and POST_ID = %s;"""


select_explore = """select POST_CONTENT,  POST_TAGS, POST_ID, USER_LOGIN, POST_DATE
               from USER_POSTS 
              where (POST_TAGS = '{0}'
                 or POST_ID  = '{0}'
                 or POST_CONTENT like '%{0}%'
                 or USER_LOGIN  = '{0}'
                 or year(POST_DATE) = '{0}'
                 or month(POST_DATE) = '{0}'
                 or day(POST_DATE) = '{0}'
                 or date(POST_DATE) = '{0}')
                and POST_STATE = 'PUB'
              limit {1} , {2};"""  

select_explore_all = """select POST_CONTENT,  POST_TAGS, POST_ID, USER_LOGIN, POST_DATE
                          from USER_POSTS
                         where POST_STATE = 'PUB'
                          order by POST_DATE desc
                          limit {0} , {1}; """


select_user_info = """select USER_LOGIN, USER_ROLE, USER_EMAIL, REG_DATE, AVATARS_PATH from USERS where USER_LOGIN = %s;"""
