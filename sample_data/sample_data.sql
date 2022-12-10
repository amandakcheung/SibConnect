----Inserting Sample Data------
use sibconn_db;

drop table if exists comment;
drop table if exists post;
drop table if exists category;
drop table if exists user;


CREATE TABLE `user` (
  `uid` int PRIMARY KEY AUTO_INCREMENT,
  `email` varchar(50) not null,
  `first_name` varchar(50) not null,
  `last_name` varchar(50) not null,
  `hashed` char(60),
  unique(email),
  `pronouns` varchar(20),
  `class_year` int(4),
  `interests` varchar(100)
)

ENGINE = InnoDB;


CREATE TABLE `post` (
  `pid` int PRIMARY KEY AUTO_INCREMENT,
  `uid` int,
  `type` ENUM('event_post', 'seeking_post'),
  `title` text,
  `category` int,
  `location` ENUM ('Tower Court', 'Quint/ West Side', 'New Dorms', 'Stone Davis', 'Branch (Lake House etc)', 'n/a'),
  `date_time` datetime,
  `length` int,
  `recurring` boolean,
  `capacity` int,
  `skill` int,
  `description` text
)

ENGINE = InnoDB;


CREATE TABLE `category` (
  `cid` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(30)
)

ENGINE = InnoDB;

CREATE TABLE `comment` (
  `commentid` int PRIMARY KEY AUTO_INCREMENT,
  `pid` int,
  `uid` int,
  `commenttext` text
)

ENGINE = InnoDB;

ALTER TABLE `comment` ADD FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);

ALTER TABLE `comment` ADD FOREIGN KEY (`pid`) REFERENCES `post`(`pid`);

ALTER TABLE `post` ADD FOREIGN KEY (`category`) REFERENCES `category` (`cid`);

ALTER TABLE `post` ADD FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);

