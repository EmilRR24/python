from flask import render_template, request, redirect, session, flash
from flask_app import app
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument     
from flask_app.models.user import User
from flask_app.models.transaction import Transaction
from flask_app.models.gamer import Gamer
from flask_app.models.game import Game

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
    flash("Account Created! Please Log In!")
    return redirect(f'/account/{user_id}')

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
    dataId = user_in_db.id
    return redirect(f'/account/{dataId}')

# ! ////// LOGOUT //////
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged Out')
    return render_template("home.html")

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/account/add/<int:id>',methods=['POST'])
def add_points(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data = id
    user_data = {
        "user_id": request.form['user_id'],
        "total_points": request.form['total_points'],
        "activity": request.form['activity'],
        "points": request.form['points'],
    }
    # Call the save @classmethod on User
    Transaction.save_transaction(user_data)
    amount = {
        "amount" : (int(request.form['total_points'])+int(request.form['points'])),
        "user_id" : int(request.form['user_id'])
    }
    print("amount is",amount)
    User.update_points(amount)
    return redirect(f'/add/{data}')

@app.route('/account/spend/<int:id>',methods=['POST'])
def spend_points(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data = id
    if not User.validate_points(request.form):
        return redirect(f'/spend/{data}')
    user_data = {
        "user_id": request.form['user_id'],
        "total_points": request.form['total_points'],
        "activity": request.form['activity'],
        "points": request.form['points'],
    }
    # Call the save @classmethod on User
    Transaction.save_transaction(user_data)
    amount = {
        "amount" : (int(request.form['total_points'])-int(request.form['points'])),
        "user_id" : int(request.form['user_id'])
    }
    print("amount is",amount)
    User.update_points(amount)
    return redirect(f'/spend/{data}')

@app.route('/gamer/register/<int:id>',methods=['POST'])
def register_gamer(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data = id
    gamer_data = {
        "user_id": request.form['user_id'],
        "stream_link": request.form['stream_link'],
    }
    # Call the save @classmethod on User
    Gamer.save_gamer(gamer_data)
    session['stream_link'] = request.form['stream_link']
    return redirect(f'/start/{data}')

@app.route('/gamer/start/<int:id>',methods=['POST'])
def gamer_start(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')

    gamer_data = {
        "introduction": request.form['introduction'],
    }
    # Call the save @classmethod on User
    session['introduction'] = request.form['introduction']
    return redirect("/gamer/start")

@app.route('/gamer/start')
def gamer_start_page():
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    return render_template("show_gamer.html")

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
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    return render_template('games_list.html')

@app.route('/account/')
def account():
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data = session.get('user')
    return render_template(f'/account/{data}')

@app.route('/transactions/<int:id>')
def transactions_history(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data ={ 
        "id":id
    }
    user=User.get_one(data)
    tr_count = len(user.transactions)
    return render_template("transactions.html", user=user, tr_count=tr_count)


# TODO READ ONE
@app.route('/account/<int:id>')
def dashboard(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data ={ 
        "id":id
    }
    user=User.get_one(data)
    tr_count = len(user.transactions)
    return render_template('account.html', user=user, tr_count=tr_count)

@app.route('/add/<int:id>')
def add(id):
    data ={ 
        "id":id
    }
    user=User.get_one(data)
    tr_count = len(user.transactions)
    return render_template("add_points.html",user=user, tr_count=tr_count)

@app.route('/spend/<int:id>')
def spend(id):
    data ={ 
        "id":id
    }
    user=User.get_one(data)
    tr_count = len(user.transactions)
    return render_template("spend_points.html",user=user, tr_count=tr_count)

@app.route('/start/<int:id>')
def start(id):
    data ={ 
        "id":id
    }
    gamer_in_db = Gamer.get_one_with_gamer(data)
    session['stream_link'] = gamer_in_db.stream_link
    return render_template("gamer_register.html",user=User.get_one(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/gamer/update/<int:id>',methods=['POST'])
def edit_stream(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    user_data = {
        "user_id": int(request.form['user_id']),
        "stream_link": request.form['stream_link'],
    }
    print(user_data)
    Gamer.update_stream(user_data)
    session['stream_link'] = request.form['stream_link']
    return redirect(f'/start/{id}')

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/user/update',methods=['POST'])
def update():
    User.update(request.form)
    return redirect('/users')

# ! ///// DELETE //////
@app.route('/account/destroy/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data ={
        'id': id
    }
    User.destroy(data)
    session.clear()
    flash('Account Deleted!')
    return redirect('/')