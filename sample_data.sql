
drop table if exists user;
drop table if exists seeking_post;
drop table if exists event_post;
drop table if exists comment;
drop table if exists category;


CREATE TABLE `user` (
  `uid` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(30),
  `email` varchar(60),
  `pronouns` varchar(20),
  `class_year` int(4)
);

CREATE TABLE `seeking_post` (
  `pid` int PRIMARY KEY,
  `uid` int,
  `category` int,
  `description` text
);

CREATE TABLE `event_post` (
  `pid` int PRIMARY KEY,
  `uid` int,
  `category` int,
  `location` ENUM ('tower', 'quint', 'new_dorms', 'stone_d', 'branch'),
  `date_time` timedate,
  `length` int,
  `recurring` boolean,
  `capacity` int,
  `skill` int,
  `description` text
);

CREATE TABLE `category` (
  `cid` int PRIMARY KEY,
  `name` varchar(30)
);

CREATE TABLE `comment` (
  `commentid` int PRIMARY KEY,
  `pid` int,
  `uid` int,
  `commenttext` text
);

ALTER TABLE `comment` ADD FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);

ALTER TABLE `event_post` ADD FOREIGN KEY (`category`) REFERENCES `category` (`cid`);

ALTER TABLE `seeking_post` ADD FOREIGN KEY (`category`) REFERENCES `category` (`cid`);

ALTER TABLE `seeking_post` ADD FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);

ALTER TABLE `event_post` ADD FOREIGN KEY (`uid`) REFERENCES `user` (`uid`);

ALTER TABLE `seeking_post` ADD FOREIGN KEY (`pid`) REFERENCES `comment` (`pid`);

ALTER TABLE `event_post` ADD FOREIGN KEY (`pid`) REFERENCES `comment` (`pid`);
