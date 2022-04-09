# install flask to directory everytime (hello_flask)
from flask import Flask, render_template, request, redirect, session  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.secret_key = 'keep it secret, keep it safe' # set a secret key for security purposes

#ADD CODE HERE
#  ! our index route will handle rendering our form
@app.route('/')          # The "@" decorator associates this route with the function immediately following
def index():
    # return render_template('index.html')
    return render_template("index.html")

# ! our create_user route will handle the input from our form
@app.route('/users', methods=['POST']) # The          # The "@" decorator associates this route with the function immediately following
def index():
    print(request.form)
    session['user_name'] = request.form['user_name']
    session['form_data'] = request.form['data']
    return redirect('/')





    # app.run(debug=True) should be the very last statement! 
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.