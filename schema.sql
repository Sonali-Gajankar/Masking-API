create table issues(
id int primary key auto_increment,
body varchar(500)
);

create table user(
id int primary key auto_increment,
username varchar(200) not null,
password varchar(200) not null,
mask_prv boolean not null
);