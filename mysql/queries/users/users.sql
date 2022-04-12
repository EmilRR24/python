-- Query: Create 3 new users

insert into users(id, first_name, last_name, email, created_at, updated_at)
values(1, "John", "Doe", "john.doe@yahoo.com", now(), now() );

insert into users(id, first_name, last_name, email, created_at, updated_at)
values(2, "Jane", "Doe", "jane.doe@yahoo.com", now(), now() );

insert into users(id, first_name, last_name, email, created_at, updated_at)
values(3, "John", "Smith", "john.smith@yahoo.com", now(), now() );

-- Query: Retrieve all the users

select * from users;

-- Query: Retrieve the first user using their email address

select * from users where email = "john.doe@yahoo.com";

-- Query: Retrieve the last user using their id

select * from users where id = 3;

-- Query: Change the user with id=3 so their last name is Pancakes

update users set
last_name = "Pancakes"
where id = 3;

-- Query: Delete the user with id=2 from the database

delete from users 
where id = 2;

-- Query: Get all the users, sorted by their first name

select * from users
order by first_name desc;

-- BONUS Query: Get all the users, sorted by their first name in descending order

select * from users
order by first_name desc;

-- Submit your .txt file that contains all the queries you ran in the workbench