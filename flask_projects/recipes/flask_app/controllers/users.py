from flask import render_template, request, redirect, session, flash
from flask_app import app
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
from flask_bcrypt import Bcrypt    
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument  
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

# ! ////// REGISTER WITH BCRYPT  //////
@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate(request.form):
        return redirect('/')
    if User.get_by_email(request.form):
        flash("Email already in use!")
        return redirect('/')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash,
        "password_confirm" : request.form['password_confirm']
    }
    # Call the save @classmethod on Model
    user_id = User.save(data)
    # store model id into session
    session['user_id'] = user_id
    session['first_name'] = request.form.get('first_name')
    session['logged_in'] = True
    return redirect("/dashboard")

# ! ////// LOGIN //////
@app.route('/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('invalid credentials')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('invalid password')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['logged_in'] = True
    return redirect('/dashboard')

# ! ////// LOGOUT //////
@app.route('/logout')
def logout():
    session.clear()
    return render_template("logout.html")

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/recipe/new')
def new():
    return render_template("add_recipe.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/register/recipe',methods=['POST'])
def register_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/new')
    Recipe.save_recipe(request.form)
    return redirect('/dashboard')

# ! ////// READ/RETRIEVE //////
# TODO ROOT ROUTE
@app.route('/')
def index():
    return render_template('register.html')

# TODO READ ALL
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", recipes = Recipe.get_all())

# TODO READ ONE
@app.route('/recipe/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("show_recipe.html",recipe=Recipe.get_one(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/recipe/edit/<int:id>')
def edit(id):
    data ={ 
        "id":id
    }
    return render_template("edit_recipe.html",recipe=Recipe.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/recipe/update',methods=['POST'])
def update():
    data = request.form.get('id')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/edit/{data}')
    Recipe.update(request.form)
    return redirect('/dashboard')

# ! ///// DELETE //////
@app.route('/recipe/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')