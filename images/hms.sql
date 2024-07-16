create database hospital_management_system;
use hospital_management_system;
show tables;
create table patient(p_id int primary key auto_increment , p_email varchar(50) ,  p_name varchar(50) not null , gender char(8) not null , address varchar(50) not null , password varchar(1000)); 
create table doctors(d_id int primary key auto_increment , d_email varchar(50) ,  d_name varchar(50) not null , d_gender char(8) not null , d_address varchar(50) not null ,Experties varchar(30) not null , d_password varchar(1000));
create table schedules(s_id  int primary key auto_increment , start_time time not null , end_time time not null , break_time time default '12:00' , scheduling_date date not null );
select * from patient;
select * from doctors;
select * from schedules;
select * from appointment;
create table appointment(a_id int primary key auto_increment , start_time time not null , end_time time not null , diag_date date not null , status varchar(3) default 'No');
create table visiting(v_id int primary key auto_increment , p_email varchar (50) references patient(p_email) , concerns varchar(50) not null ,symptoms varchar(50) not null , p_id int  references patient(p_id));
create table medication(m_id int primary key auto_increment ,  precautions varchar(150) , medications varchar(150) , v_id int references visiting(v_id));
create table history(h_id int primary key auto_increment 