from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import flash


class Productivity:
    def __init__(self, data):
        self.id = data['id']
        self.hours_sleep = data['hours_sleep']
        self.ate_breakfast = data['ate_breakfast']
        self.gym = data['gym']
        self.overall_happiness = data['overall_happiness']
        self.overall_productivity = data['overall_productivity']
        self.comments = data['comments']
        self.date = data['date']
        if data['user_id']:
            self.user = users.User.get_one({"id":data['user_id']})
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(post_data):
        is_valid = True
        if not post_data['hours_sleep']:
            flash('Hours slept cannot be empty!', 'hours_sleep')
            is_valid = False
        elif len(post_data['hours_sleep']) < 0:
            flash('Hours slept cannot be below 0!', 'hours_sleep')
            is_valid = False
        if not post_data['ate_breakfast']:
            flash('Cannot leave this field blank!', 'ate_breakfast')
            is_valid = False
        if not post_data['gym']:
            flash('Cannot leave this field blank!', 'gym')
            is_valid = False
        if len(post_data['overall_happiness']) < 0 or len(post_data['overall_happiness']) > 10:
            flash('Must enter a valid number!', 'overall_happiness')
            is_valid = False
        if len(post_data['overall_productivity']) < 0 or len(post_data['overall_productivity']) > 10:
            flash('Must enter a valid number!', 'overall_productivity')
            is_valid = False
        if len(post_data['date']) < 8 or not post_data['date']:
            flash('Date must be valid!', 'date')
            is_valid = False
        return is_valid
        
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO productivity (hours_sleep, ate_breakfast, gym, overall_happiness, overall_productivity, comments, date, user_id, created_at, updated_at)
        VALUES (%(hours_sleep)s, %(ate_breakfast)s, %(gym)s, %(overall_happiness)s, %(overall_productivity)s, %(comments)s, %(date)s, %(user_id)s, NOW(), NOW());
        """
        result = connectToMySQL('productivity_schema').query_db(query, data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM productivity WHERE id = %(id)s;"
        result = connectToMySQL('productivity_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM productivity;"
        results = connectToMySQL('productivity_schema').query_db(query)
        days = []
        for row in results:
            days.append(cls(row))
        return days
    
    @classmethod
    def update(cls, data):
        query = """
        UPDATE productivity
        SET hours_sleep = %(hours_sleep)s, ate_breakfast = %(ate_breakfast)s, gym = %(gym)s, overall_happiness = %(overall_happiness)s,
        overall_productivity = %(overall_productivity)s, comments = %(comments)s, date= %(date)s, updated_at = NOW()
        WHERE id = %(id)s;
        """
        result = connectToMySQL('productivity_schema').query_db(query, data)
        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM productivity WHERE id = %(id)s"
        result = connectToMySQL('productivity_schema').query_db(query, data)
        return result