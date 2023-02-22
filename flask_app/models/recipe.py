from flask_app.config.mysqlconnection import connectToMySQL
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Recipe:
    db = "recipe_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.minute = data['minute']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name,description,instruction,minute,date,user_id) VALUES(%(name)s,%(description)s,%(instruction)s,%(minute)s,%(date)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, minute=%(minute)s, date=%(date)s, user_id=%(user_id)s ,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters","recipe")
            is_valid=False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters","recipe")
            is_valid=False
        if len(recipe['instruction']) < 3:
            flash("Instruction must be at least 3 characters","recipe")
            is_valid= False
        if recipe['date'] == "":
            flash("Please enter a date","recipe")
            is_valid= False
        return is_valid