from flask import render_template, request, redirect, session, flash
from flask_app import app
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
from flask_bcrypt import Bcrypt  
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument     
from flask_app.models.user import User
from flask_app.models.transaction import Transaction
from flask_app.models.game import Game
from flask_app.models.bet import Bet
from flask_app.models.twitch_api import get_twitch

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
    if User.get_by_stream_link(request.form):
        flash("Stream Link is already registered!")
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
        "stream_link": request.form['stream_link'],
        "password" : pw_hash,
        "total_points": 0,
    }

    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['user_id'] = user_id
    session['user_name'] = request.form.get('user_name')
    session['stream_link'] = request.form.get('stream_link')
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
    return redirect("/")

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
# ! ////// ADD POINTS//////
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

# ! ////// SPEND POINTS //////
@app.route('/account/spend/<int:id>',methods=['POST'])
def spend_points(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    data = {'id':id}
    user=User.get_one(data)
    if int(request.form['points']) > user.total_points:
        flash("Not Enough Points In Your Account!")
        return redirect(f'/spend/{id}')
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
    User.update_points(amount)
    return redirect(f'/spend/{id}')

# ! ////// GAMER START/GAMER UPDATE //////
@app.route('/gamer/start/<int:id>',methods=['POST'])
def gamer_start(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    # Call the save @classmethod on User
    session['introduction'] = request.form['introduction']
    return redirect(f'/gamer/show/{id}')

@app.route('/gamer/show/<int:id>')
def gamer_start_page(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    id={'id':id}
    games=get_twitch()['data']
    data = []
    for game in games:
        if game['name'] != "Just Chatting":
            if game['name'] != "Music":
                if game['name'] != "Slots":
                    data.append({'name' : game['name'], 'id' : game['id']})
    print(games)
    history=Game.get_all_with_gamer(id)
    tr_count = len(history)
    return render_template("show_gamer.html", games=history, tr_count=tr_count, titles=data )


# ! ////// PLACE BET //////
@app.route('/bet/select/<name>')
def select_bet(name):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    game_name=name
    games=get_twitch()['data']
    data = []
    for game in games:
        if game['name'] == game_name:
            data.append({'box_art_url': game['box_art_url'].format(width=250,height=250),'name' : game['name'], 'id' : game['id']})
    game=data[0]
    # print(game)
    return render_template("bet_type.html", game=game)

@app.route('/bet/select/<select>/<name>')
def select_type(select, name):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    select=select
    game_name=name
    games=get_twitch()['data']
    data = []
    for game in games:
        if game['name'] == game_name:
            data.append({'box_art_url': game['box_art_url'].format(width=250,height=250),'name' : game['name'], 'id' : game['id']})
    game=data[0]
    id={'id':session['user_id']}
    user=User.get_one(id)
    return render_template("place_bet.html", game=game, select=select, user=user)

@app.route('/start/game/<select>/<name>',methods=['POST'])
def place_bet(select, name):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    select=select
    game_name=name
    games=get_twitch()['data']
    data = []
    for game in games:
        if game['name'] == game_name:
            data.append({'box_art_url': game['box_art_url'].format(width=250,height=250),'name' : game['name'], 'id' : game['id']})
    game=data[0]
    id={'id':session['user_id']}
    user=User.get_one(id)
    bet=Bet.save_bet(request.form)
    return render_template("show_bet.html", game=game, select=select, user=user, bet=bet)




# ! ////// CREATE GAME //////
@app.route('/start/game/<int:id>',methods=['POST'])
def start_game(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    Game.start_game(request.form)
    data = {'id': id}
    game_in_db = Game.get_one_with_gamer(data)
    flash('Game Started!')
    session['game_id'] = game_in_db.id
    return redirect(f"/gamer/show/{id}")

# ! ////// COMPLETE GAME //////
@app.route('/complete/game/<int:id>',methods=['POST'])
def complete_game(id):
    Game.game_complete(request.form)
    flash('Game Completed!')
    session.pop('game_id')
    return redirect(f'/gamer/show/{id}')

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
    games=get_twitch()['data']
    data = []
    for game in games:
        if game['name'] != "Just Chatting":
            if game['name'] != "Music":
                if game['name'] != "Slots":
                    data.append({'box_art_url': game['box_art_url'].format(width=250,height=250),'name' : game['name'], 'id' : game['id']})
    # print(f'data: {data}')
    return render_template('games_list.html', games=data)

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
    print(id)
    data = {'id':id}
    return render_template("gamer_register.html", gamer=User.get_one(data))

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
    if User.get_by_stream_link(request.form):
        flash("Stream Link is already registered!")
        return redirect('/register')
    User.update_stream(user_data)
    flash("Stream Link Updated!")
    session['stream_link'] = request.form['stream_link']
    return redirect(f'/start/{id}')

@app.route('/user/update/<int:id>',methods=['POST'])
def edit_user(id):
    if 'user_id' not in session:
        flash('Please login!')
        return redirect('/')
    user_data = {
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "user_name": request.form['user_name'],
    }
    if User.get_by_user_name(request.form):
        flash("User Name is already registered!")
        return redirect(f'/account/{id}')
    User.update_user(user_data)
    session['user_name'] = request.form.get('user_name')
    flash("Account Updated!")
    return redirect(f'/account/{id}')

# TODO ONE TO HANDLE THE DATA FROM THE FORM
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