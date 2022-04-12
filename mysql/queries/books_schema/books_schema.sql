Query: Create 5 different authors: Jane Austen, Emily Dickinson, Fyodor Dostoevsky, William Shakespeare, Lau Tzu

INSERT INTO authors(name)
VALUES ("Jane Austen"), ("Emily Dickinson"), ("Fyodor Dostoevsky"), ("William Shakespeare"), ("Lau Tzu");

Query: Create 5 books with the following names: C Sharp, Java, Python, PHP, Ruby

INSERT INTO books(title)
VALUES ("C Sharp"), ("Java"), ("Python"), ("PHP"), ("Ruby");

Query: Change the name of the C Sharp book to C#

UPDATE books 
SET title = "C#"
WHERE id = 1;

Query: Change the first name of the 4th author to Bill

UPDATE authors
SET name = "Bill Shakespeare"
WHERE id = 4;

Query: Have the first author favorite the first 2 books

INSERT INTO favorite_books(author_id, book_id)
VALUES (1, 1), (1, 2);

Query: Have the second author favorite the first 3 books

INSERT INTO favorite_books(author_id, book_id)
VALUES (2, 1), (2, 2), (2,3);

Query: Have the third author favorite the first 4 books

INSERT INTO favorite_books(author_id, book_id)
VALUES (3, 1), (3, 2), (3, 3), (3, 4);

Query: Have the fourth author favorite all the books

INSERT INTO favorite_books(author_id, book_id)
VALUES (4, 1), (4, 2), (4, 3), (4, 4), (4, 5);

Query: Retrieve all the authors who favorited the 3rd book

SELECT * FROM books_schema.favorite_books
WHERE book_id = 3;

Query: Remove the first author of the 3rd book's favorites

DELETE from favorite_books
where book_id = 3 and id = 5;

Query: Add the 5th author as an other who favorited the 2nd book

INSERT INTO favorite_books(author_id, book_id)
VALUES (5, 2);

Find all the books that the 3rd author favorited

INSERT INTO favorite_books(author_id, book_id)
VALUES (5, 2);

Query: Find all the authors that favorited to the 5th book

SELECT * FROM favorite_books
WHERE book_id = 5;
