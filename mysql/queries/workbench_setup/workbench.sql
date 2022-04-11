select * from dojos;

insert into dojos(id, name, created_at, updated_at)
values(1, "Burbank", now(), now()) ;

insert into dojos(id, name, created_at, updated_at)
values(2, "SanJose", now(), now()) ;

update dojos set
name = "San Jose"
where id = 2;

insert into dojos(id, name, created_at, updated_at)
values(3, "Honolulu", now(), now()) ;

delete from dojos 
where id = 3;
