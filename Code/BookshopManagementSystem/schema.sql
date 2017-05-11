drop table if exists books;
create table books(
	id integer primary key autoincrement,
	bookid text not null,
	title text not null,
	author text,
	inventory integer,
	salenum integer,
	bid double,
	price double,
	description text
);