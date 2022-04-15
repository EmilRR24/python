# import the function that will return an instance of a connection
from flask_app.models.ninja import Ninja
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
DATABASE = 'dojos_and_ninjas'

class Dojo:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(DATABASE).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
            
    @classmethod
    def save(cls, data ):
        print(data)
        query = "INSERT INTO dojos (name) VALUES ( %(name)s);"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(DATABASE).query_db( query, data )
        return result

        @classmethod
        def get_one(cls,data:dict) -> object:
            query  = "SELECT * FROM dojos WHERE id = %(id)s";
            result = connectToMySQL(DATABASE).query_db(query,data)
            return cls(result[0])

    @classmethod
    def get_one_with_ninjas(cls, data ):
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON dojos.id = ninjas.dojo_id WHERE dojos.id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        dojo = cls(results[0])
        for ninja in results:
            ninja_data = {
            'id': ninja['ninjas.id'],
            'first_name':ninja['first_name'],
            'last_name':ninja['last_name'],
            'age':ninja['age'],
            'dojo_id':ninja['dojo_id'],
            'created_at':ninja['ninjas.created_at'],
            'updated_at':ninja['ninjas.updated_at']
            }
            dojo.ninjas.append(Ninja(ninja_data))
        print(dojo.name)
        return dojo

    @classmethod
    def update(cls, data):
        query = "UPDATE dojos SET name = %(name)s;"
        result = connectToMySQL(DATABASE).query_db( query, data )
        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM dojos WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db( query, data )
        return result