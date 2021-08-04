from flask import flash, render_template, redirect, session, url_for, request
from flask_app import app
from flask_app.models.users import User, Productivity
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create', methods = ['POST'])
def create_user():
    if not User.validate(request.form):
        return redirect('/')
    hash_browns = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password' : hash_browns
    }
    print(data)
    user_id = User.create(data)
    session['uuid'] = user_id
    print(request.form)
    return redirect('/dashboard')


@app.route('/login', methods = ['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_by_email({'email' : request.form['email']})
    session['uuid'] = user.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')