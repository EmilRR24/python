from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'website_project' # enter the name of the database you want to use

class Transaction:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.activity = data['activity']
        self.points = data['points']
        self.bet_id = data['bet_id']
        self.created_at = data['created_at']
        if "user_id" in data:
            self.user_id = data['user_id']
        if "total_points" in data:
            self.total_points = data['total_points']


    # ! CREATE
    @classmethod
    def save_transaction(cls, data:dict) -> int:
        query = "INSERT INTO transactions (activity,points,user_id) VALUES (%(activity)s,%(points)s,%(user_id)s);"
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

