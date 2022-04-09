# install flask to directory everytime (hello_flask)
from flask import Flask, render_template, request, redirect, session # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
app.secret_key = 'keep it secret, keep it safe' 
#ADD CODE HERE
@app.route('/')          # The "@" decorator associates this route with the function immediately following
def dojo_survey():
    return render_template('index.html')  # Return the string 'Hello World!' as a response

@app.route('/survey', methods=['POST'])
def create_user():
    print(request.form)
    session['name'] = request.form['name']
    session['location'] = request.form['location']
    session['languages'] = request.form['languages']
    session['comment'] = request.form['comment']
    session['sex'] = request.form['sex']
    session['student'] = request.form['student']
    return redirect('/result')

@app.route('/result')
def result():
    return render_template('index1.html')



    # app.run(debug=True) should be the very last statement! 
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.