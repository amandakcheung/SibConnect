--- Adding Sample Data to Database sibconn----

use sibconn_db;
source sample_data.sql;

insert into user(email, first_name, last_name, hashed, pronouns, class_year, `dorm`, interests)
values 
('joe@wellesley.edu', 'Joe', 'Dou','12345', 'he/him', 2022, 'beebe', 'music'),
('amy@wellesley.edu', 'Amy', 'Lee', '12345', 'she/her', 2026, 'tower west', 'Language & Culture'),
('matt@wellesley.edu', 'Matt', "Anderson", '12345', 'they/them', 2023, 'freeman', 'Arts & Crafts');

insert into category(name)
values
('Music'),
('Arts & Crafts'),
('Language & Culture'),
('Other');

insert into post(uid, type, title, category, location, date_time,length, recurring, capacity, skill, description)
values
(2, 'seeking_post', 'watercoloring!', 2, NULL, NULL, NULL, NULL, NULL, NULL, 'want to watercolor with someone' ),
(1, 'seeking_post', 'sing together?', 1, NULL, NULL, NULL, NULL, NULL, NULL, 'want to learn how to sing with other people' ),
(3, 'event_post', 'come paint the sky!!', 2, 'Quint/ West Side', '2022-12-01 12:00:00', 60, false, 30, 0, 'painting the sky'),
(1, 'event_post', 'come learn spanish with us!', 3, 'Tower Court', '2023-01-30 11:30:00', 120, true, 15, 2, 'spanish table');


insert into comment(pid, uid, commenttext)
values
( 4, 1, 'looking forward to it!'),
( 3, 2, 'interested in learning with u');

insert into interested(uid, pid)
values
(2, 4),
(3, 1),
(2, 3),
(2, 2),
(1, 1);
