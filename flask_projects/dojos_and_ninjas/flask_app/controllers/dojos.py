from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.dojo import Dojo


@app.route('/')
def index_dojos():
    dojos = Dojo.get_all()
    return render_template('indexDojos.html', dojos = dojos)

@app.route('/show')
def show_dojos():
    dojos = Dojo.get_all()
    return render_template('show_dojos.html', dojos = dojos)

@app.route('/show_user/<int:id>')
def show_dojo(id):
    data = {'id': id}
    Dojo.get_one(data)
    return render_template('/show_dojo.html', dojo = Dojo.get_one(data))

@app.route('/delete/<int:id>')
def delete_user(id):
    data = {'id': id}
    Dojo.delete(data)
    return redirect('/')

@app.route('/create_dojo', methods=['POST'])
def create_dojo():
    id = Dojo.save(request.form)
    return redirect(f"/show_dojo/{id}" )


@app.route('/update_dojo/<int:id>')
def update_dojo(id):
    data = {'id': id}
    return render_template('update_dojo.html', dojo = Dojo.get_one(data))

@app.route('/update_dojo2/<int:id>', methods=['POST'])
def update_dojo2(id):
    print(request.form)
    data = {"name":request.form['name'], "id": id }
    Dojo.update(data)
    return redirect(f"/show_dojo/{id}")