import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash('First Name is required.')
            is_valid = False
        if len(user['last_name']) < 1:
            flash('Last Name is required.')
            is_valid = False
        if len(user['email']) < 1:
            flash('Email is required.')
            is_valid = False
        if len(user['email']) > 0:
            if not EMAIL_REGEX.match(user['email']):
                flash('Invalid email format.')
                is_valid = False    
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('users').query_db(query,user)
        if len(results) != 0:
            flash('This email is already being used.')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash('First Name is required.')
            is_valid = False
        if len(user['last_name']) < 1:
            flash('Last Name is required.')
            is_valid = False
        if len(user['email']) < 1:
            flash('Email is required.')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format.')
            is_valid = False
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('users').query_db(query,user)
        if results[0]['email'] == user['email']:
            return is_valid        
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('users').query_db(query,user)
        if len(results) != 0:
            flash('This email is already being used.')
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    # Display single user info
    @classmethod
    def get_one_user(cls,data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """
        return connectToMySQL('users').query_db(query,data)

    # Set up query to add new users into our database
    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO users (first_name, last_name, email, created_at, updated_at) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW()); 
                """
        return connectToMySQL('users').query_db(query,data)

    # Set up query to update user's info in our database
    @classmethod
    def update(cls,data):
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, created_at = NOW(), updated_at = NOW()
                WHERE id = %(id)s;
                """
        return connectToMySQL('users').query_db(query,data)

    # Set up query to delete users from our database
    @classmethod
    def delete(cls,data):
        query = """
                DELETE FROM users
                WHERE id = %(id)s;
                """
        return connectToMySQL('users').query_db(query,data)