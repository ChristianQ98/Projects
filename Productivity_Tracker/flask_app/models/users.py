from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re
from flask_app.models.productivity import Productivity


bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.dob = data['dob']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        products = []


    # VALIDATION FOR REGISTRATION
    @staticmethod
    def validate(post_data):
        is_valid = True
        # Checks if first name has 2 characters or more
        if len(post_data['first_name']) < 2:
            flash('First name must be 2 characters or more!', 'first_name')
            is_valid = False
        # Checks if last name has 2 characters or more
        if len(post_data['last_name']) < 2:
            flash('Last name must be 2 characters or more!', 'last_name')
            is_valid = False
        # Checks if date of birth is valid, by ensuring that it has 9 digits
        if len(post_data['dob']) < 8:
            flash('Please enter a valid Date of Birth!', 'dob')
            is_valid = False
        # Checks if email is formatted properly
        if not EMAIL_REGEX.match(post_data['email']):
            flash('Please enter a valid email!', 'email')
            is_valid = False
        # Checks if email is already in use by another user
        elif User.get_by_email({'email':post_data['email']}):
            flash('Email is already in use!', 'email')
            is_valid = False
        # Checks if password meets the criteria to ensure that it is a strong password
        if not PASSWORD_REGEX.match(post_data['password']):
            flash('Password must contain at least one uppercase character, one lowercase character, one number, one special character, and at least eight total characters','password')
            is_valid = False
        # Checks if passwords match
        elif post_data['password'] != post_data['confirm_password']:
            flash('Passwords must match!', 'password')
            is_valid = False
        return is_valid

        
    # VALIDATION FOR LOGIN
    @staticmethod
    def validate_login(post_data):
        is_valid = True
        user = User.get_by_email({'email':post_data['email']})
        if not user:
            flash('Access Denied!','category2')
            return False
        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash('Access Denied!','category2')
            return False
        return is_valid


    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, dob, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(dob)s, %(email)s, %(password)s, NOW(), NOW());"
        result = connectToMySQL('productivity_schema').query_db(query,data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('productivity_schema').query_db(query, data)
        user = cls(result[0])
        return user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('productivity_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE users
        SET first_name = %(first_name)s, last_name = %(last_name)s, dob = %(dob)s, email = %(email)s, password = %(password)s, updated_at = NOW()
        WHERE id = %(id)s;
        """
        result = connectToMySQL('productivity_schema').query_db(query, data)
        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        result = connectToMySQL('productivity_schema').query_db(query, data)
        return result

    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('productivity_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])