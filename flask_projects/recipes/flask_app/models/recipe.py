from asyncio.windows_events import NULL
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'cookbook' # enter the name of the database you want to use

class Recipe:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.cooktime = data['cooktime']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.user_id = data['user_id']

    # ! RECIPE VALIDATIONS
    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM recipes WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching recipe
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_recipe(recipe:dict) -> bool:
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if len(recipe['instruction']) < 3:
            flash("Instruction must be at least characters.")
            is_valid = False
        if len(recipe['date_made']) < 1:
            flash("Must have a date made.")
            is_valid = False

        return is_valid

    # ! CREATE
    @classmethod
    def save_recipe(cls, data:dict) -> int:
        query = "INSERT INTO recipes (name, cooktime, description, instruction, date_made, user_id) VALUES (%(name)s,%(cooktime)s,%(description)s, %(instruction)s, %(date_made)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for u in results:
            recipes.append( cls(u) )
        return recipes
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM recipes WHERE id = %(id)s";
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    # ! READ/RETRIEVE LEFT JOIN
    @classmethod
    def get_one_with_users(cls, data ):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.id = users.recipe_id WHERE recipes.id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        recipe = [cls(results[0])]
        for user in results:
            user_data = {
            'id': user['users.id'],
            'name':user['name'],
            'cooktime':user['users.cooktime'],
            'description':user['description'],
            'instruction':user['instruction'],
            'date_made':user['users.date_made'],
            'user_id':user['user_id']
            }
            recipe.users.append(User(user_data))
        return recipe

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s,instruction=%(instruction)s,date_made=%(date_made)s,cooktime=%(cooktime)s) WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)