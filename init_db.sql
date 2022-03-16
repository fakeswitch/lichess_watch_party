create database watch_lichess;

use watch_lichess;

create table watch_users(handle varchar(255), status bool,id int not null unique AUTO_INCREMENT Primary key);

insert into watch_users(handle, status)
values
('fake_switch',False),
('DrNykterstein',False),
('FourLanChurro',False),
('Jelle1',False),
('PostalBeef',False),
('prostidude',False),
('Friedwing',False),
('LuckBeOnYourSide',False),
('frostypanda37',False),
('FiveBucks',False),
('HoldMyRooks',False);
