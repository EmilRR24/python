# Flask Checklist

- [x] create a separate directory for each app.
- [x] inside the directory for the app, run:

```bash
pipenv install flask=='2.0.3' pymysql
```
- [x] activate the virtual environment and install bcrypt:

```bash
pipenv shell
pipenv install werkzeug==2.0.3 flask==2.0.3 flask-bcrypt
```
- [x] add [server.py](server.py) with the following content:

```py
from flask_app import app
from flask_app.controllers import models

if __name__ == "__main__":
    app.run(debug=True)
```

- [x] add [flask_app](./flask_app/__init__.py) with the `__init__.py` file that contains the following:

```py
from flask import Flask, session

app = Flask(__name__)
```

- [x] add [mysqlconnection.py](./flask_app/config/mysqlconnection.py) to the `config` directory inside the `flask_app` package. It should contain the following:

```py
import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):

        connection = pymysql.connect(host = 'localhost',
                                    model = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)

        self.connection = connection
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close() 

def connectToMySQL(db):
    return MySQLConnection(db)
```

- [x] add the models for the application inside the `models` directory. Each non-relational table in the database should have a [model](flask_app/models/model.py). A generic model should look like this:

```py
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re    # the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = 'checklist' # enter the name of the database you want to use

class Model:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.column1 = data['column1']
        self.column2 = data['column2']
        self.column3 = data['column3']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # ! VALIDATIONS
    @classmethod
    def get_by_email(cls,data:dict) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate(user:dict) -> bool:
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if not (user['first_name'].isalpha()):
            flash("First name must be letters!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not (user['last_name'].isalpha()):
            flash("Last name must be letters")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['password_confirm']:
            flash("Passwords do not match.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    # ! CREATE
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO models (column1,column2,column3) VALUES (%(column1)s,%(column2)s,%(column3)s);"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result

    # ! READ/RETRIEVE ALL
    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM models;"
        results = connectToMySQL(DATABASE).query_db(query)
        models = []
        for u in results:
            models.append( cls(u) )
        return models
    
    # ! READ/RETRIEVE ONE
    @classmethod
    def get_one(cls,data:dict) -> object:
        query  = "SELECT * FROM models WHERE id = %(id)s";
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    # ! UPDATE
    @classmethod
    def update(cls,data:dict) -> int:
        query = "UPDATE models SET column1=%(column1)s,column2=%(column2)s,column3=%(column3)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    # ! DELETE
    @classmethod
    def destroy(cls,data:dict):
        query  = "DELETE FROM models WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

```

- [x] add the controllers for the app routes inside [flask_app/controllers/models.py](flask_app/controllers/models.py):
```py

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
    return redirect('/models')

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
```

- [x] add the view of MVC:
  - [ ] add [models.html](flask_app/templates/models.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>models</title>
</head>
<body>
    <h1 class="text-center">Here are our models!!!</h1>
    <table class="table table-hover">
        <thead>
            <tr>
                <th>Column One</th>
                <th>Column Two</th>
                <th>Column Three</th>
                <th>Created At</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for model in models %}
            <tr>
                <td>{{ model.column1 }}</td>
                <td>{{ model.column2 }}</td>
                <td>{{ model.column3}}</td>
                <td>{{ model.created_at.strftime("%b %d %Y") }}</td>
                <td>
                    <a href="/model/show/{{ model.id }}">Show</a> |
                    <a href="/model/edit/{{ model.id }}">Edit</a> |
                    <a href="/model/destroy/{{ model.id }}">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <a href="/model/new" class="btn btn-primary">Add a model</a>
</body>
</html>
```

  - [x] add [new_model.html](flask_app/templates/new_model.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>Create model</title>
</head>
<body>
    <!-- this is for flash messages -->
    {% with messages = get_flashed_messages() %}
    {% if messages %}
    {% for message in messages %}
    <p>{{message}}</p>
    {% endfor %}
    {% endif %}
    {% endwith %}

    <form action="/model/create" method="post" class="col-6 mx-auto">
        <h2 class="text-center">Add model</h2>
        <div class="form-group">
            <label for="column1">column1:</label>
            <input type="text" name="column1"  class="form-control">
        </div>
        <div class="form-group">
            <label for="column2">column2:</label>
            <input type="text" name="column2"  class="form-control">
        </div>
        <div class="form-group">
            <label for="column3">column3:</label>
            <input type="text" name="column3"  class="form-control">
        </div>
        <input type="submit" value="Add model" class="btn btn-success">
    </form>
</body>
</html>
```

  - [x] add [show_model.html](flask_app/templates/show_model.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>model</title>
</head>
<body>
    <h2 class="text-center">model {{model.id}}</h2>
    <p>column1 {{model.column1}}</p>
    <p>column2: {{model.column2}}</p>
    <p>column3: {{model.column3}}</p>

    <p>Created ON: {{model.created_at.strftime("%b %d %Y")}}</p>
    <p>Last Updated: {{  model.updated_at.strftime("%b %d %Y")}}</p>
</body>
</html>
```

  - [x] add [edit_model.html](flask_app/templates/edit_model.html):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <title>Edit model</title>
</head>
<body>

    <form action="/model/update" method="post" class="col-6 mx-auto">
        <h2 class="text-center">Edit {{model.id}}</h2>
        <input type="hidden" name="id" value={{model.id}}>
        <div class="form-group">
            <label for="column1">column1:</label>
            <input type="text" name="column1"  class="form-control" value="{{model.column1}}">
        </div>
        <div class="form-group">
            <label for="column2">column2:</label>
            <input type="text" name="column2" class="form-control" value="{{model.column2}}">
        </div>
        <div class="form-group">
            <label for="column3">column3:</label>
            <input type="text" name="column3"  class="form-control" value="{{model.column3}}">
        </div>
        <input type="submit" value="Update model" class="btn btn-success">
    </form>
</body>
</html>
```