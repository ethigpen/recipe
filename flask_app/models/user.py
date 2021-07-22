from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_app.models.recipe import Recipe


class User():

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []


    @classmethod
    def create_user(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        new_user = connectToMySQL('recipe').query_db(query, data)
        return new_user

    @classmethod
    def get_user_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('recipe').query_db(query,data)
        user_email = []
        for item in results:
            user_email.append(User(item))
        return user_email

    @staticmethod
    def validate_user_info(info):
        is_valid = True
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$") 
        if len(info['first_name'])< 3 or len(info['first_name'])> 45:
            flash ("First name must be between 3 and 45 characters long.")
            is_valid = False
        if len(info['last_name'])< 3 or len(info['last_name'])> 45:
            flash ("Last name must be between 3 and 45 characters long.")
            is_valid = False
        if not email_regex.match(info['email']):
            flash("Invalid email address! Try again!")
            is_valid = False
        if len(User.get_user_email({'email': info['email']})) !=0:
            flash("This email address is already in use. Try again!")
            is_valid = False
        if len(info['password'])< 8:
            flash ("Password must be at least 8 characters long")
            is_valid = False
        if info['password'] != info['password_confirm']:
            flash ("Password and Confirm Password do not match.")
            is_valid = False
        return is_valid
        