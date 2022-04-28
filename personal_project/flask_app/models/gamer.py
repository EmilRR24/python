from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'website_project' # enter the name of the database you want to use

class Gamer:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.stream_link = data['stream_link']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        self.user_id = data['user_id']
        if "total_points" in data:
            self.total_points = data['total_points']


    # ! CREATE
    @classmethod
    def save_gamer(cls, data:dict) -> int:
        query = "INSERT INTO gamer (stream_link,user_id) VALUES (%(stream_link)s,%(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM transaction;"
        results = connectToMySQL(DATABASE).query_db(query)
        transactions = []
        for u in results:
            transactions.append( cls(u) )
        return transactions

    # ! UPDATE

    @classmethod
    def update_stream(cls,data:dict) -> int:
        query = "UPDATE gamer SET stream_link=%(stream_link)s,updated_at=NOW() WHERE user_id = %(user_id)s;"
        result =  connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        return result
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM gamers WHERE id = %(id)s";
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

