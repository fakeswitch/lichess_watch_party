use watch_lichess;

create table followers(lichess_name varchar(255), discord_id varchar(255),id int not null unique AUTO_INCREMENT Primary key);
