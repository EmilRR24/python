# install flask to directory everytime (hello_flask)
from flask import Flask, render_template, request, redirect, session  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

#ADD CODE HERE
@app.route('/')          # The "@" decorator associates this route with the function immediately following
def index():
    if 'count' not in session:
        session['views'] += 1
        session['count'] = 0
    return render_template("index.html") 

@app.route('/destroy_session')
def destroy():
    session.pop('count')
    return redirect('/')

@app.route('/up')
def up():
    session['count'] += 1
    return redirect('/')

@app.route('/down')
def down():
    session['count'] -= 1
    return redirect('/')

@app.route('/up_2')
def up_2():
    session['count'] += 2
    return redirect('/')




    # app.run(debug=True) should be the very last statement! 
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.