from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'login_registration' # enter the name of the database you want to use

class User:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
        ## ! used in user validation
    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate(user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if not (user['first_name'].isalpha()):
            flash("First name must be letters!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not (user['last_name'].isalpha()):
            flash("Last name must be letters")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['password_confirm']:
            flash("Passwords do not match.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for u in results:
            users.append( cls(u) )
        return users
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM users WHERE id = %(id)s";
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,password=%(password)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)


