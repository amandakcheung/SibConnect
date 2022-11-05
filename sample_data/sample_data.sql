----Inserting Sample Data------
use sibconn_db;

drop table if exists comment;
drop table if exists post;
drop table if exists category;
drop table if exists user;


CREATE TABLE `user` (
  `uid` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(30),
  `email` varchar(60),
  `pronouns` varchar(20),
  `class_year` int(4)
)

ENGINE = InnoDB;


CREATE TABLE `post` (
  `pid` int PRIMARY KEY,
  `uid` int,
  `type` ENUM('event_post', 'seeking_post'),
  `category` int,
  `location` ENUM ('tower', 'quint', 'new_dorms', 'stone_d', 'branch', 'n/a'),
  `date_time` datetime,
  `length` int,
  `recurring` boolean,
  `capacity` int,
  `skill` int,
  `description` text
)

ENGINE = InnoDB;


CREATE TABLE `category` (
  `cid` int PRIMARY KEY,
  `name` varchar(30)
)

ENGINE = InnoDB;

CREATE TABLE `comment` (
  `commentid` int PRIMARY KEY,
  `pid` int,
  `uid` int,
  `commenttext` text,
  index(pid)
)

ENGINE = InnoDB;


ALTER TABLE `comment` ADD FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);

ALTER TABLE `comment` ADD FOREIGN KEY (`pid`) REFERENCES `post`(`pid`);

ALTER TABLE `post` ADD FOREIGN KEY (`category`) REFERENCES `category` (`cid`);

ALTER TABLE `post` ADD FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);
