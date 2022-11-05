--- Adding Sample Data to Database sibconn----

use sibconn_db;
source sample_data.sql;

insert into user(uid, name, email, pronouns, class_year)
values (1, 'joe', 'joe@wellesley.edu', 'he/him', 2022);

insert into user(uid, name, email, pronouns, class_year)
values (2, 'amy', 'amy@wellesley.edu', 'she/her', 2026);

insert into user(uid, name, email, pronouns, class_year)
values (3, 'matt', 'matt@wellesley.edu', 'they/them', 2023);

insert into category(cid, name)
values(1, 'music');

insert into category(cid, name)
values(2, 'art');

insert into category(cid, name)
values(3, 'language');

insert into post(pid, uid, type, category, location, date_time,length, recurring, capacity, skill, description)
values(1, 2, 'seeking_post', 2, NULL, NULL, NULL, NULL, NULL, NULL, 'want to watercolor with someone' );

insert into post(pid, uid, type, category, location, date_time,length, recurring, capacity, skill, description)
values(2, 1, 'seeking_post', 1, NULL, NULL, NULL, NULL, NULL, NULL, 'want to learn how to sing with other people' );

insert into post(pid, uid, type, category, location, date_time,length, recurring, capacity, skill, description)
values(3, 2, 'seeking_post', 3, NULL, NULL, NULL, NULL, NULL, NULL, 'want to watercolor with someone' );

insert into post(pid, uid, type, category, location, date_time,length, recurring, capacity, skill, description)
values(4, 3, 'event_post', 2, 'quint', '2022-12-01 12:00:00', 60, false, 30, 0, 'painting the sky');

insert into post(pid, uid, type, category, location, date_time,length, recurring, capacity, skill, description)
values(5, 1, 'event_post', 3, 'tower', '2023-01-30 11:30:00', 120, true, 15, 2, 'spanish table');

insert into comment(commentid, pid, uid, commenttext)
values(1, 5, 1, 'looking forward to it!');

insert into comment(commentid, pid, uid, commenttext)
values(2, 3, 2, 'interested in learning with u');