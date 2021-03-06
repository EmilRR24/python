-- Forward engineer the dojos_and_ninjas_schema from the previous chapter

-- Create a .txt file where you'll save each of your queries from below

-- Query: Create 3 new dojos
insert into dojos(id, name, created_at, updated_at)
values(1, "Burbank", now(), now()) ;

insert into dojos(id, name, created_at, updated_at)
values(2, "SanJose", now(), now()) ;

insert into dojos(id, name, created_at, updated_at)
values(3, "Chicago", now(), now()) ;

-- Query: Delete the 3 dojos you just created
delete from dojos 
where id = 1;

delete from dojos 
where id = 2;

delete from dojos 
where id = 3;

-- Query: Create 3 more dojos
insert into dojos(id, name, created_at, updated_at)
values(1, "Burbank", now(), now()) ;

insert into dojos(id, name, created_at, updated_at)
values(2, "SanJose", now(), now()) ;

insert into dojos(id, name, created_at, updated_at)
values(3, "Chicago", now(), now()) ;

-- Query: Create 3 ninjas that belong to the first dojo
insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(1, "Emil", "Ramirez", 35, now(), now(), 1);

insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(4, "Jane", "Doe", 35, now(), now(), 1);

insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(5, "John", "Smith", 35, now(), now(), 1);

-- Query: Create 3 ninjas that belong to the second dojo
insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(2, "Ryan", "Flemming", 35, now(), now(), 2);

insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(6, "Jane", "Smith", 35, now(), now(), 2);

insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(7, "Tiger", "Woods", 35, now(), now(), 2);

-- Query: Create 3 ninjas that belong to the third dojo
insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(1, "Aaron", "Phillips", 35, now(), now(), 3);

insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(8, "Rory", "McIlroy", 35, now(), now(), 3);

insert into ninjas(id, first_name, last_name, age, created_at, updated_at, dojo_id)
values(9, "Rory", "McIlroy", 35, now(), now(), 3);
-- Query: Retrieve all the ninjas from the first dojo
select * from ninjas
where dojo_id =1;

-- Query: Retrieve all the ninjas from the last dojo
select * from ninjas
where dojo_id =2;

-- Query: Retrieve the last ninja's dojo
select * from ninjas
where dojo_id =3;

-- Submit your .txt file that contains all the queries you ran in the shell