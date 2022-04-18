from flask import render_template, request, redirect, session, flash
from flask_app import app
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument


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
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    session['first_name'] = request.form.get('first_name')
    session['logged_in'] = True
    return redirect("/users")

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
    return redirect('/users')

@app.route('/logout')
def logout():
    session.clear()
    return render_template("logout.html")

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/user/create')
def new():
    return render_template("new_user.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
# @app.route('/user/create',methods=['POST'])
# def create():
#     print(request.form)
#     User.save(request.form)
#     return redirect('/register/user')

# ! ////// READ/RETRIEVE //////
# TODO ROOT ROUTE
@app.route('/')
def index():
    return render_template('users.html')

# TODO READ ALL
@app.route('/users')
def users():
    return render_template("user_index.html",users=User.get_all())

# TODO READ ONE
@app.route('/user/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("show_user.html",user=User.get_one(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/user/edit/<int:id>')
def edit(id):
    data ={ 
        "id":id
    }
    return render_template("edit_user.html",user=User.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/user/update',methods=['POST'])
def update():
    if not User.validate(request.form):
        userId = request.form.get('id')
        return redirect(f'/user/edit/{userId}')
    User.update(request.form)
    return redirect('/users')

# ! ///// DELETE //////
@app.route('/user/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    User.destroy(data)
    return redirect('/users')