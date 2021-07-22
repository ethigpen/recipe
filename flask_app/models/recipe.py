from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re

class Recipe():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def create_recipe(cls,data):
        query= 'INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30)s, %(user_id)s );'
        new_recipe_id = connectToMySQL('recipe').query_db(query, data)
        return new_recipe_id

    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL('recipe').query_db(query)
        recipes = []
        for item in results:
            new_recipe = Recipe(item)
            recipes.append(new_recipe)
        return recipes

    @classmethod
    def get_recipe(cls,data):
        query= 'SELECT * FROM recipes WHERE id = %(id)s;'
        results = connectToMySQL('recipe').query_db(query, data)
        recipe = Recipe(results[0])
        return recipe

    @classmethod
    def update_recipe(cls,data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(id)s;'
        recipe_id = connectToMySQL('recipe').query_db(query, data)
        return recipe_id

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        return connectToMySQL('recipe').query_db(query,data)

    @staticmethod
    def validate_recipe(info):
        is_valid = True
        date_regex = re.compile(r"^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.]\d\d$")
        if len(info['name'])< 3 or len(info['name'])> 45:
            flash ("Recipe name must be between 3 and 45 characters long.")
            is_valid = False
        if len(info['description'])< 3 or len(info['description'])> 45:
            flash ("Description must be between 3 and 45 characters long.")
            is_valid = False
        if len(info['instructions'])< 3 or len(info['instructions'])> 2000:
            flash ("Instructions must be between 3 and 2,000 characters long.")
            is_valid = False
        if not date_regex.match(info['date_made']):
            flash("Give the date in the proper format dd/mm/yy")
            is_valid = False
        return is_valid