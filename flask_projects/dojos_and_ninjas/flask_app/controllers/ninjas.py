from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.ninja import Ninja


@app.route('/ninjas')
def index_ninjas():
    ninjas = Ninja.get_all()
    return render_template('indexNinjas.html', ninjas = ninjas)

@app.route('/show_ninjas')
def show_ninjas():
    ninjas = Ninja.get_all()
    return render_template('showNinjas.html', ninjas = ninjas)

@app.route('/show_ninja/<int:id>')
def show_ninja(id):
    data = {'id': id}
    Ninja.get_one(data)
    return render_template('/showNinja.html', ninja = Ninja.get_one(data))

@app.route('/delete_ninja/<int:id>')
def delete_ninja(id):
    data = {'id': id}
    Ninja.delete(data)
    return redirect('/ninjas')

@app.route('/create_ninja', methods=['POST'])
def create_ninja():
    id = Ninja.save(request.form)
    return redirect(f"/showNinja/{id}" )


@app.route('/update_ninja/<int:id>')
def update_ninja(id):
    data = {'id': id}
    return render_template('update_ninja.html', user = Ninja.get_one(data))

@app.route('/update_ninja2/<int:id>', methods=['POST'])
def update_ninja2(id):
    print(request.form)
    data = {"first_name":request.form['first_name'],
    "last_name":request.form['last_name'], "email":request.form['email'], "id": id }
    Ninja.update(data)
    return redirect(f"/showNinja/{id}")