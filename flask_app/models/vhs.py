from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class VHS:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.poster_id = data['poster_id']
        self.owner_id = data['owner_id']

        self.poster = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM vhses JOIN users ON users.id = poster_id ORDER BY vhses.updated_at DESC;"
        results = connectToMySQL('vhses_schema').query_db(query)

        if len(results) == 0:
            return 0
        else:
            vhses = []

            for row_in_db in results:
                one_vhs = cls(row_in_db)

                user_data = {
                    "id" : row_in_db['users.id'],
                    "first_name" : row_in_db['first_name'],
                    "last_name" : row_in_db['last_name'],
                    "email" : row_in_db['email'],
                    "password" : row_in_db['password'],
                    "address" : row_in_db['address'],
                    "city" : row_in_db['city'],
                    "state" : row_in_db['state'],
                    "zip" : row_in_db['zip'],
                    "created_at" : row_in_db['users.created_at'],
                    "updated_at" : row_in_db['users.updated_at'],
                }
                one_vhs.poster = user.User(user_data)
                vhses.append(one_vhs)
            return vhses
	
    @classmethod
    def save(cls, data):
        query = "INSERT INTO vhses (title, price, created_at, updated_at, poster_id , owner_id) VALUES ( %(title)s , %(price)s , NOW() , NOW() , %(poster_id)s , %(owner_id)s );"
        return connectToMySQL('vhses_schema').query_db(query, data)

    @classmethod
    def get_vhs(cls, data):
        query = "SELECT * FROM vhses JOIN users ON users.id = poster_id WHERE vhses.id = %(id)s ;"
        results = connectToMySQL('vhses_schema').query_db(query, data)

        one_vhs = cls( results[0])

        user_data = {
            "id" : results[0]['users.id'],
            "first_name" : results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "address" : results[0]['address'],
            "city" : results[0]['city'],
            "state" : results[0]['state'],
            "zip" : results[0]['zip'],
            "created_at" : results[0]['users.created_at'],
            "updated_at" : results[0]['users.updated_at']
        }

        one_vhs.poster = user.User(user_data)
        return one_vhs

    @classmethod
    def update(cls, data):
        query = "UPDATE vhses SET price = %(price)s , updated_at = NOW() WHERE id = %(id)s ;"
        return connectToMySQL('vhses_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
	    query = "DELETE FROM vhses WHERE id = %(id)s;"
	    return connectToMySQL('vhses_schema').query_db( query, data )

    @classmethod
    def buy(cls, data):
        query = "UPDATE vhses SET updated_at = NOW() , owner_id = %(owner_id)s WHERE id = %(id)s ;"
        return connectToMySQL('vhses_schema').query_db(query, data)

    @staticmethod
    def validate_vhs( data ):
        is_valid = True	

        if len(data['title']) < 3:
            flash("The title is too short!")
            is_valid = False
        if data['price'] == '':
            flash("Price field is empty!")
            is_valid = False     
        if is_valid == True: 
            flash("Your submission was successful!")
                
        return is_valid	