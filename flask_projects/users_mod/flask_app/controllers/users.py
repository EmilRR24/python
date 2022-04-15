from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.user import User


@app.route('/')
def index():
    users = User.get_all()
    return render_template('index.html', users = users)

@app.route('/show')
def show():
    users = User.get_all()
    return render_template('show.html', users = users)

@app.route('/show_user/<int:id>')
def show_user(id):
    data = {'id': id}
    return render_template('/show_user.html', user = User.get_one(data))

@app.route('/delete/<int:id>')
def delete_user(id):
    data = {'id': id}
    User.delete(data)
    return redirect('/')

@app.route('/create_friend', methods=['POST'])
def create_friend():
    id = User.save(request.form)
    return redirect(f"/show_user/{id}" )


@app.route('/update/<int:id>')
def update(id):
    data = {'id': id}
    return render_template('update.html', user = User.get_one(data))

@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    print(request.form)
    data = {"first_name":request.form['first_name'],
    "last_name":request.form['last_name'], "email":request.form['email'], "id": id }
    User.update(data)
    return redirect(f"/show_user/{id}")