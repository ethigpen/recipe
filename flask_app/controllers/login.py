from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/user', methods = ["POST"])
def register_user():
        if not User.validate_user_info(request.form):
            return redirect('/')
        data ={
            'first_name': request.form['first_name'],
            'last_name': request.form ['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        user = User.create_user(data)
        session['id']= user
        session['first_name']= request.form['first_name']
        return redirect('/')

@app.route('/login/user', methods=["POST"])
def login_user():
    users = User.get_user_email(request.form)
    if len(users)!= 1:
        flash('User does not exist. Please register!')
        return redirect('/')
    user = users[0]
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Password for the given user is incorrect.")
        return redirect('/')
    session['id']= user.id
    session['first_name']= user.first_name
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        flash('Please log in to view this page')
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', recipes = recipes)

@app.route('/logout/user')
def logout_user():
    session.clear()
    return redirect('/')

@app.route('/recipes/new')
def new_recipe():
    if 'id' not in session:
        flash('Please log in to view this page')
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data={
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30'],
        'user_id': session['id']
    }
    Recipe.create_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    data ={
            'id': id
        }
    recipe = Recipe.get_recipe(data)
    return render_template('show_recipe.html', recipe = recipe)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    data = {
        'id' : id
    }
    recipe = Recipe.get_recipe(data)
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_made': request.form['date_made'],
        'under_30': request.form['under_30']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def delete(id):
    data={
            'id': id
        }
    Recipe.delete(data)
    return redirect('/dashboard')