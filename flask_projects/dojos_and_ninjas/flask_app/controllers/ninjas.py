from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.ninja import Ninja
from flask_app.models.dojo import Dojo



@app.route('/create_ninja', methods=['POST'])
def create_ninja():
    Ninja.save(request.form)
    data = request.form.get('dojo_id')
    print(data)
    return redirect(f'/show/{data}')

@app.route('/ninjas')
def index_ninjas():
    return render_template('indexNinjas.html', dojos = Dojo.get_all())

@app.route('/show/<int:id>')
def show_dojo(id):
    data = {'id': id}
    return render_template('showDojo.html', dojo = Dojo.get_one_with_ninjas(data))

@app.route('/dojos')
def index_dojos():
    dojos = Dojo.get_all()
    return render_template('indexDojos.html', dojos = dojos)

@app.route('/create_dojo', methods=['POST'])
def create_dojo():
    Dojo.save(request.form)
    return redirect('/dojos')
