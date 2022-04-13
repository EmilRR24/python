Query: Create 6 new users

INSERT INTO users(first_name, last_name)
VALUES ("Jane", "Does"), ("John", "Doe"), ("John", "Smith"), ("Ben", "Lublin"), ("Ryan", "Flemming"), ("Aaron", "Phillips");

Query: Have user 1 be friends with user 2, 4 and 6



Query: Have user 2 be friends with user 1, 3 and 5

Query: Have user 3 be friends with user 2 and 5

Query: Have user 4 be friends with user 3

Query: Have user 5 be friends with user 1 and 6

Query: Have user 6 be friends with user 2 and 3

Query: Display the relationships create as shown in the above image

NINJA Query: Return all users who are friends with the first user, make sure their names are displayed in results.

NINJA Query: Return the count of all friendships

NINJA Query: Find out who has the most friends and return the count of their friends.

NINJA Query: Return the friends of the third user in alphabetical order