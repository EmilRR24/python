# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
DATABASE = 'dojos_and_ninjas'

class Ninja:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dojo_id = data['dojo_id']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
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
        query = "INSERT INTO ninjas ( first_name , last_name , age , created_at, updated_at, dojo_id ) VALUES ( %(first_name)s , %(last_name)s , %(age)s , NOW() , NOW(), %(dojo_id)s  );"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(DATABASE).query_db( query, data )
        return result

    @classmethod
    def get_one(cls, data ):
        query = "SELECT * FROM ninjas WHERE dojo_id = %(id)s ORDER BY id DESC;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        ninjas = []
        for ninja in results:
            ninjas.append( cls(ninja) )
        print(ninjas)
        return ninjas
    @classmethod
    def update(cls, data):
        query = "UPDATE ninjas SET first_name = %(first_name)s , last_name = %(last_name)s, age = %(age)s WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db( query, data )
        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM ninjas WHERE id = %(id)s"
        result = connectToMySQL(DATABASE).query_db( query, data )
        return result