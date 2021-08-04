from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_app.models.users import User, Productivity


@app.route('/dashboard')
def dashboard():
    all_days = Productivity.get_all()
    return render_template('dashboard.html', logged_in_user = User.get_one({'id' : session['uuid']}), all_days = all_days)


@app.route('/add_day')
def create_log():
    return render_template('log_day.html', logged_in_user = User.get_one({'id' : session['uuid']}))


@app.route('/log_day', methods = ['POST'])
def log_day():
    if 'uuid' not in session:
        return redirect('/')
    if not Productivity.validate(request.form):
        return redirect('/add_day')
    data = {
        **request.form,
        'user_id' : session['uuid']
    }
    Productivity.create(data)
    return redirect('/dashboard')


@app.route('/day/<int:id>/view')
def view_day(id):
    if 'uuid' not in session:
        return redirect('/')
    return render_template('view_day.html', logged_in_user = User.get_one({'id' : session['uuid']}), day = Productivity.get_one({'id' : id}))


@app.route('/day/<int:id>/edit')
def edit_day(id):
    if 'uuid' not in session:
        return redirect('/')
    return render_template('edit_day.html', logged_in_user = User.get_one({'id' : session['uuid']}), day = Productivity.get_one({'id' : id}))


@app.route('/day/<int:id>/update', methods = ['POST'])
def update_day(id):
    if not Productivity.validate(request.form):
        return redirect(f'day/{id}/edit')
    post_data = {
        **request.form,
        'id' : id
    }
    Productivity.update(post_data)
    return redirect('/dashboard')


@app.route('/day/<int:id>/delete')
def delete_day(id):
    if 'uuid' not in session:
        return redirect('/')
    Productivity.delete({'id' : id})
    return redirect('/dashboard')


@app.template_filter('datetimeformat')
def datetimeformat(value, format="%B"):
    return value.strftime(format)