from flask import render_template, request, redirect, session, flash
from flask_app import app
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument     
from flask_app.models.user import User

# ! ////// REGISTER WITH BCRYPT  //////
@app.route('/register/user', methods=['POST'])
def register():
    # validate the form here ...
    if not User.validate(request.form):
        return redirect('/register')
    if User.get_by_email(request.form):
        flash("Email already in use!")
        return redirect('/register')
    if User.get_by_user_name(request.form):
        flash("User Name is taken!")
        return redirect('/register')
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "user_name": request.form['user_name'],
        "password" : pw_hash,
        "total_points": 0,
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    session['user_name'] = request.form.get('user_name')
    session['logged_in'] = True
    return redirect("/account")

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
    session['user_name'] = user_in_db.user_name
    session['logged_in'] = True
    return redirect('/account')

# ! ////// LOGOUT //////
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged Out')
    return render_template("home.html")

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/user/new')
def new():
    return render_template("new_user.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/user/create',methods=['POST'])
def create():
    print(request.form)
    User.save(request.form)
    return redirect('/users')

# ! ////// READ/RETRIEVE //////
# TODO ROOT ROUTE
@app.route('/')
def index():
    return render_template('home.html')

# TODO READ ALL
@app.route('/register')
def registration():
    return render_template('register.html')

# TODO READ ALL
@app.route('/games')
def games_list():
    return render_template('games_list.html')

# TODO READ ONE
@app.route('/account/<int:id>')
def dashboard(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data ={ 
        "id":id
    }
    return render_template('account.html', user=User.get_one(data))

@app.route('/add/<int:id>')
def add(id):
    data ={ 
        "id":id
    }
    return render_template("add_points.html",user=User.get_one(data))

@app.route('/spend/<int:id>')
def spend(id):
    data ={ 
        "id":id
    }
    return render_template("spend_points.html",user=User.get_one(data))

@app.route('/start/<int:id>')
def start(id):
    data ={ 
        "id":id
    }
    return render_template("gamer_register.html",user=User.get_one(data))

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