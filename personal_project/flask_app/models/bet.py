from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'website_project' # enter the name of the database you want to use

class Bet:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.game_id = data['game_id']
        self.action = data['action']
        self.bet_amount = data['bet_amount']
        self.created_at = data['created_at']
        self.completed_at = data['completed_at']

    # ! CREATE
    @classmethod
    def save_bet(cls, data:dict) -> int:
        query = "INSERT INTO bets (game_id,action,bet_amount) VALUES (%(game_id)s,%(action)s,%(bet_amount)s);"
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
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM models WHERE id = %(id)s";
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
