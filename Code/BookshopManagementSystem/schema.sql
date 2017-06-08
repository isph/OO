drop table if exists books;
drop table if exists account;
drop table if exists orderform;
drop table if exists reserve;
drop table if exists history;
create table books(
	id integer primary key autoincrement,
	bookid text not null,
	title text not null,
	author text,
	inventory integer,
	salenum integer,
	bid double,
	price double,
	description text,
	discount double,
	time double,
	bundle text,
	type text,
	backup text
);

create table account(
	id integer primary key autoincrement,
	type text,
	email text,
  username text,
	password text,
	money double,
	backup text
);

create table orderform(
	id integer PRIMARY KEY AUTOINCREMENT,
	type text,
	bookname text,
	booknum integer,
	fixprice double,
	bidprice double,
  validtime integer,
  state text,
	bookpos text,
	address text,
	name text,
	phone text,
	backup text
);

create TABLE reserve(
	id integer PRIMARY KEY AUTOINCREMENT,
	type text,
	bookname text,
	isbn text,
	author text,
	user text,
	backup text
);

create table history(
	id integer primary key autoincrement,
	userid text not null,
	bookid text not null,
	title text not null,
	author text,
	inventory integer,
	salenum integer,
	bid double,
	price double,
	description text,
	discount double,
	time double,
	bundle text,
	type text,
	backup text
);

INSERT INTO account (type, username, password, money) VALUES ('1', 'admin', 'pass', 10000);

INSERT INTO account (type, username, password, money) VALUES ('2', 'customer', 'pass', 1000);

INSERT INTO account (type, username, password, money) VALUES ('3', 'supplier', 'pass', 5000);