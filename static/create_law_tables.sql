create database if not exists paper;
use paper;

create table i_law_list_resume(
    thread_id tinyint unsigned primary key,
    last_query char(255),
    last_query_hashed char(32),
    page_index tinyint unsigned,
    tag tinyint unsigned default 0
);

insert into i_law_list_resume(thread_id, last_query, last_query_hashed, page_index) values(0, 'initial', 'initial', 0);
insert into i_law_list_resume(thread_id, last_query, last_query_hashed, page_index) values(1, 'initial', 'initial', 0);
insert into i_law_list_resume(thread_id, last_query, last_query_hashed, page_index) values(2, 'initial', 'initial', 0);
insert into i_law_list_resume(thread_id, last_query, last_query_hashed, page_index) values(3, 'initial', 'initial', 0);
insert into i_law_list_resume(thread_id, last_query, last_query_hashed, page_index) values(4, 'initial', 'initial', 0);


create table i_law_single_0(
    id int unsigned primary key auto_increment,
    lid char(64) not null,
    title text,
    authority text,
    law_level char(10),
    number text,
    post_date char(12),
    eff_date char(12),
    status char(10)
);

create table i_law_single_1(
    id int unsigned primary key auto_increment,
    lid char(64) not null,
    title text,
    authority text,
    law_level char(10),
    number text,
    post_date char(12),
    eff_date char(12),
    status char(10)
);

create table i_law_single_2(
    id int unsigned primary key auto_increment,
    lid char(64) not null,
    title text,
    authority text,
    law_level char(10),
    number text,
    post_date char(12),
    eff_date char(12),
    status char(10)
);

create table i_law_single_3(
    id int unsigned primary key auto_increment,
    lid char(64) not null,
    title text,
    authority text,
    law_level char(10),
    number text,
    post_date char(12),
    eff_date char(12),
    status char(10)
);

create table i_law_single_4(
    id int unsigned primary key auto_increment,
    lid char(64) not null,
    title text,
    authority text,
    law_level char(10),
    number text,
    post_date char(12),
    eff_date char(12),
    status char(10)
);



