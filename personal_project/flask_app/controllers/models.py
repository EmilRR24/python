from flask import render_template, request, redirect, session, flash
from flask_app import app
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes
from flask_bcrypt import Bcrypt      
from flask_app.models.model import Model

# ! ////// REGISTER WITH BCRYPT  //////
@app.route('/register/model', methods=['POST'])
def register():
    # validate the form here ...
    if not Model.validate(request.form):
        return redirect('/')
    if Model.get_by_email(request.form):
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
    model_id = Model.save(data)
    # store model id into session
    session['model_id'] = model_id
    session['first_name'] = request.form.get('first_name')
    session['logged_in'] = True
    return redirect("/models")

# ! ////// LOGIN //////
@app.route('/login', methods=['post'])
def login():
    data = {'email': request.form['email']}
    model_in_db = Model.get_by_email(data)
    if not model_in_db:
        flash('invalid credentials')
        return redirect('/')
    if not bcrypt.check_password_hash(model_in_db.password, request.form['password']):
        flash('invalid password')
        return redirect('/')
    session['model_id'] = model_in_db.id
    session['first_name'] = model_in_db.first_name
    session['logged_in'] = True
    return redirect('/models')

# ! ////// CREATE  //////
# TODO CREATE REQUIRES TWO ROUTES:
# TODO ONE TO DISPLAY THE FORM:
@app.route('/model/new')
def new():
    return render_template("new_model.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/model/create',methods=['POST'])
def create():
    print(request.form)
    Model.save(request.form)
    return redirect('/models')

# ! ////// READ/RETRIEVE //////
# TODO ROOT ROUTE
@app.route('/')
def index():
    return render_template('home.html')

# TODO READ ALL
@app.route('/models')
def models():
    return render_template("models.html",models=Model.get_all())

# TODO READ ONE
@app.route('/model/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("show_model.html",model=Model.get_one(data))

# ! ///// UPDATE /////
# TODO UPDATE REQUIRES TWO ROUTES
# TODO ONE TO SHOW THE FORM
@app.route('/model/edit/<int:id>')
def edit(id):
    data ={ 
        "id":id
    }
    return render_template("edit_model.html",model=Model.get_one(data))

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/model/update',methods=['POST'])
def update():
    Model.update(request.form)
    return redirect('/models')

# ! ///// DELETE //////
@app.route('/model/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Model.destroy(data)
    return redirect('/models')