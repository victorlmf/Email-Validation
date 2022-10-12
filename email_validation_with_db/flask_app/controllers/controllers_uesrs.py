from flask import request, render_template, redirect, session
from flask_app import app
from flask_app.models.models_user import User

@app.route('/users')
def index():
    users = User.get_all()
    return render_template('/users.html', all_users=users)

# Add new user
@app.route('/users/new')
def user_form():
    return render_template('/create_user.html')

@app.route('/create', methods=['POST'])
def create_user():
    if User.validate_user(request.form):
        User.save(request.form)
        return redirect('/users')
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    return redirect('/users/new')

# Display user
@app.route('/users/<int:id>')
def show_user(id):
    data = {
        "id" : id
    }
    user = User.get_one_user(data)
    return render_template('/user.html',id=id, user=user[0])

# Update user
@app.route('/users/<int:id>/edit')
def edit_form(id):
    data = {
        "id" : id
    }
    user = User.get_one_user(data)
    return render_template('/edit.html', id=id, user=user[0])

@app.route('/update', methods=['POST'])
def update():
    if User.validate_update(request.form):
        User.update(request.form)
        return redirect('/users')
    user_id = request.form['id']
    return redirect(f'/users/{user_id}/edit')

# Delete user
@app.route('/users/<int:id>/delete')
def delete(id):
    data = {
        "id" : id
    }
    User.delete(data)
    return redirect('/users')