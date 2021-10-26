from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import vhs
import re
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

ADDRESS_REGEX = re.compile(r'^[#.0-9a-zA-Z\s,-]+$')

class User:
    def __init__( self , data ):
        self.id =  data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']   
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.movies = []
        self.purchases = []

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, email, password, address, city, state, zip, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s, %(address)s , %(city)s , %(state)s , %(zip)s , NOW() , NOW() );"
        return connectToMySQL("vhses_schema").query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s , email = %(email)s, password = %(password)s, address = %(address)s , city = %(city)s , state = %(state)s , zip = %(zip)s ,  updated_at = NOW() WHERE id = %(id)s ;"
        return connectToMySQL('vhses_schema').query_db(query, data)

    @classmethod
    def get_by_email(cls, data ):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("vhses_schema").query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0])  

    @classmethod 
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("vhses_schema").query_db(query,data)

        if len(result) < 1:
            return False
        return cls(result[0]) 

    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("vhses_schema").query_db(query, data)

        if len(result) < 1:
            return False
        return True 

    @classmethod
    def get_users_vhses(cls, data):
        query = "SELECT * FROM users JOIN vhses ON vhses.poster_id = users.id WHERE poster_id = %(id)s ORDER BY vhses.updated_at DESC LIMIT 6;"
        results = connectToMySQL('vhses_schema').query_db( query , data )

        if results == False:
            return False
        elif len(results) == 0:
            return 0
        else:
            user = cls(results[0])
            for row_from_db in results:
                vhses_data = {
                    "id" : row_from_db["vhses.id"],
                    "title" : row_from_db["title"],
                    "price" : row_from_db["price"],
                    "created_at" : row_from_db["vhses.created_at"],
                    "updated_at" : row_from_db["vhses.updated_at"],
                    "poster_id" : row_from_db["poster_id"],		
                    "owner_id" : row_from_db["owner_id"]			
                }
                user.movies.append(vhs.VHS( vhses_data) )
            return user

    @classmethod
    def get_full_users_vhses(cls, data):
        query = "SELECT * FROM users JOIN vhses ON vhses.poster_id = users.id WHERE poster_id = %(id)s ORDER BY vhses.updated_at DESC;"
        results = connectToMySQL('vhses_schema').query_db( query , data )

        if results == False:
            return False
        elif len(results) == 0:
            return 0
        else:
            user = cls(results[0])
            for row_from_db in results:
                vhses_data = {
                    "id" : row_from_db["vhses.id"],
                    "title" : row_from_db["title"],
                    "price" : row_from_db["price"],
                    "created_at" : row_from_db["vhses.created_at"],
                    "updated_at" : row_from_db["vhses.updated_at"],
                    "poster_id" : row_from_db["poster_id"],		
                    "owner_id" : row_from_db["owner_id"]			
                }
                user.movies.append(vhs.VHS( vhses_data) )
            return user

    @classmethod
    def get_users_purchases(cls, data):
        query = "SELECT * FROM users JOIN vhses ON vhses.owner_id = users.id WHERE owner_id = %(id)s ORDER BY vhses.updated_at DESC LIMIT 10;"
        results = connectToMySQL('vhses_schema').query_db( query , data )

        if results == False:
            return False
        elif len(results) == 0:
            return 0
        else:
            user = cls(results[0])
            for row_from_db in results:
                vhses_data = {
                    "id" : row_from_db["vhses.id"],
                    "title" : row_from_db["title"],
                    "price" : row_from_db["price"],
                    "created_at" : row_from_db["vhses.created_at"],
                    "updated_at" : row_from_db["vhses.updated_at"],
                    "poster_id" : row_from_db["poster_id"],		
                    "owner_id" : row_from_db["owner_id"]			
                }
                user.purchases.append(vhs.VHS( vhses_data) )
            return user

    @classmethod
    def get_full_users_purchases(cls, data):
        query = "SELECT * FROM users JOIN vhses ON vhses.owner_id = users.id WHERE owner_id = %(id)s ORDER BY vhses.updated_at DESC;"
        results = connectToMySQL('vhses_schema').query_db( query , data )

        if results == False:
            return False
        elif len(results) == 0:
            return 0
        else:
            user = cls(results[0])
            for row_from_db in results:
                vhses_data = {
                    "id" : row_from_db["vhses.id"],
                    "title" : row_from_db["title"],
                    "price" : row_from_db["price"],
                    "created_at" : row_from_db["vhses.created_at"],
                    "updated_at" : row_from_db["vhses.updated_at"],
                    "poster_id" : row_from_db["poster_id"],		
                    "owner_id" : row_from_db["owner_id"]			
                }
                user.purchases.append(vhs.VHS( vhses_data) )
            return user

    @classmethod
    def delete(cls, data):
	    query = "DELETE FROM users WHERE id = %(id)s;"
	    return connectToMySQL('vhses_schema').query_db( query, data )

        
    @staticmethod
    def validate_email_and_password( data ):
        is_valid = True	

        email_data = {
            "email" : data['email']
        }

        email_match = User.check_email(email_data)

        if email_match == True:
            flash("Email already exists in records!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if data['password'] != data['confirm-password']:
            flash("Passwords do not match!")
            is_valid = False
        if len(data['password']) < 5:
            flash("Passwords do not match!")
            is_valid = False
        if len(data['fname']) < 2:
            flash("First name must be at least 2 characters!")
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last name must be at least 2 characters!")
            is_valid = False
        if len(data['address']) < 7: 
            flash("Address must be at least 7 characters!")
            is_valid = False
        if not ADDRESS_REGEX.match(data['address']): 
            flash("Invalid address!")
            is_valid = False
        if len(data['city']) < 3:
            flash("City must be more than three characters!")
            is_valid = False         
        if len(data['state']) == 1:
            flash("State must be two characters!")
            is_valid = False  
        if len(data['zip']) == 4:
            flash("Zip code must be five characters!")
            is_valid = False    
        if is_valid == True:
            flash("You successfully registered!")  
                
        return is_valid	

    @staticmethod
    def validate_and_update(data):
        is_valid = True	

        email_data = {
            "email" : data['email']
        }

        if not data['email'] == data['prev_email']:
            email_match = User.check_email(email_data)
            if email_match == True:
                flash("Email already exists in records!")
                is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if data['password'] != data['confirm-password']:
            flash("Passwords do not match!")
            is_valid = False
        if len(data['password']) < 5:
            flash("Passwords do not match!")
            is_valid = False
        if len(data['fname']) < 2:
            flash("First name must be at least 2 characters!")
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last name must be at least 2 characters!")
            is_valid = False
        if len(data['address']) < 7: 
            flash("Address must be at least 7 characters!")
            is_valid = False
        if not ADDRESS_REGEX.match(data['address']): 
            flash("Invalid address!")
            is_valid = False
        if len(data['city']) < 3:
            flash("City must be more than three characters!")
            is_valid = False         
        if len(data['state']) == 1:
            flash("State must be two characters!")
            is_valid = False  
        if len(data['zip']) == 4:
            flash("Zip code must be five characters!")
            is_valid = False    
        if is_valid == True:
            flash("You successfully updated!")  
                
        return is_valid	



