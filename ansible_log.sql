create table playbook_log (
id int not null auto_increment,
task_desc varchar(100) not null,
user varchar(30) not null,
group_id varchar(50) not null,
all_log blob not null,
run_timestamp varchar(30) not null,
log_time timestamp not null default current_timestamp,
primary key (id));
