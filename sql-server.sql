create schema if not exists amir collate latin1_swedish_ci;

create table if not exists tickets
(
	id int auto_increment
		primary key,
	subject text not null,
	body text not null,
	user_related int not null,
	replay text null,
	date longtext not null,
	status text not null
);

create table if not exists users
(
	id int auto_increment
		primary key,
	username varchar(200) not null,
	password text not null,
	firstname text null,
	lastname text null,
	token text null,
	type tinyint(1) default 0 not null,
	constraint users_username_uindex
		unique (username)
);


