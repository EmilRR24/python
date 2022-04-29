from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'website_project' # enter the name of the database you want to use

class Game:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.title = data['title']
        self.result = data['result']
        self.gamer_id = data['gamer_id']
        self.created_at = data['created_at']
        self.completed_at = data['completed_at']
        # if "total_points" in data:
        #     self.total_points = data['total_points']


    # ! CREATE
    @classmethod
    def start_game(cls, data:dict) -> int:
        query = "INSERT INTO games (name,title,gamer_id) VALUES (%(name)s,%(title)s,%(gamer_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all_with_gamer(cls,data:dict) -> list:
        query = "SELECT * FROM games WHERE gamer_id=%(id)s ORDER BY id DESC;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        games = []
        for u in results:
            games.append( cls(u) )
        print(games)
        return games

    # ! UPDATE
    @classmethod
    def game_complete(cls,data:dict) -> int:
        query = "UPDATE games SET completed_at=NOW(),result=%(result)s WHERE id = %(id)s;"
        result =  connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return result
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one_with_gamer(cls,data:dict) -> object:
        query  = "SELECT * FROM games WHERE gamer_id = %(id)s ORDER BY id DESC;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return cls(result[0])

