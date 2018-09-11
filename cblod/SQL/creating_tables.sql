 CREATE USER 'admin' IDENTIFIED BY 'adminpwd';

create table USERS (
					USER_ROLE  char(4)   not null default 'USER',
					USER_LOGIN char(15)  not null,
					USER_EMAIL char(100) not null, 
					USER_PWD   char(50)  not null,
					REG_DATE   datetime  not null default CURRENT_TIMESTAMP,
					primary key (USER_LOGIN),
                    unique(USER_EMAIL)
                    
);

create table test_table (
					POST_ID    char(14)  not null auto_increment,
					USER_ROLE  char(4)   not null default 'USER',
					USER_LOGIN char(15)  not null,
					USER_EMAIL char(100) not null, 
					USER_PWD   char(50)  not null,
					REG_DATE   datetime  not null default CURRENT_TIMESTAMP,
					primary key (ID)
);

create table USER_POSTS (
    POST_ID      bigint     not null auto_increment,
    USER_LOGIN   char(15)   not null,
    POST_DATE    datetime   not null default CURRENT_TIMESTAMP, 
    POST_CONTENT text not null,
    POST_TAGS    char(100)  not null default 'unmarked',
    primary key (POST_ID),
    unique(USER_EMAIL)
)
;
commit;



drop table test_table;
commit;
