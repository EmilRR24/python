from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.transaction import Transaction
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


DATABASE = 'website_project' # enter the name of the database you want to use

class User:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.user_name = data['user_name']
        self.password = data['password']
        self.total_points = data['total_points']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if "points" in data:
            self.points = data['points']
        self.transactions = []

    # ! VALIDATIONS
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
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(user['user_name']) < 2:
            flash("User name must be at least 2 characters.")
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

    @staticmethod
    def validate_points(user:dict) -> bool:
        is_valid = True
        if user['points'] > user['total_points']:
            flash("Not Enough Points In Your Account!")
            is_valid = False
        return is_valid

    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO users (first_name,last_name,email,user_name,password,total_points) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(user_name)s,%(password)s,%(total_points)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

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
        query  = "SELECT * FROM users LEFT JOIN transactions ON users.id = transactions.user_id WHERE users.id = %(id)s ORDER BY transactions.id DESC";
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            user = cls(results[0])
            for data in results:
                tr_data = {
                    "id" : data['transactions.id'],
                    "activity" : data['activity'],
                    "points" : data['points'],
                    "bet_id" : data['bet_id'],
                    "created_at" : data['transactions.created_at']
                }
                user.transactions.append(Transaction(tr_data)) 
        return user

    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching email
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def get_by_user_name(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE user_name = %(user_name)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching user_name
        if len(result) < 1:
            return False
        return cls(result[0])


    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,user_name=%(user_name)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update_points(cls,data:dict) -> int:
        query = "UPDATE users SET total_points=%(amount)s,updated_at=NOW() WHERE id = %(user_id)s;"
        result =  connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return result
    


    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)