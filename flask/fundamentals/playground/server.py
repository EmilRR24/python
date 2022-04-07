# install flask to directory everytime (hello_flask)
from flask import Flask, render_template  # Import Flask to allow us to create our app
app = Flask(__name__)    # Create a new instance of the Flask class called "app"
#ADD CODE HERE

@app.route('/play')          # The "@" decorator associates this route with the function immediately following
def index():
    return render_template("index.html", phrase='', times=5, color="lightblue")

@app.route('/play/<int:x>')          # The "@" decorator associates this route with the function immediately following
def index1(x):
    return render_template("index.html", phrase='', times=x, color="lightblue")
@app.route('/play/<int:x>/<color>')          
def index2(x, color):
    return render_template("index.html", phrase='', times=x, color=color)


    # app.run(debug=True) should be the very last statement! 
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.