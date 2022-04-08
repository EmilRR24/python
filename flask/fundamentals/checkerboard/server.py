# install flask to directory everytime (hello_flask)
from flask import Flask, render_template  # Import Flask to allow us to create our app
import math
app = Flask(__name__)    # Create a new instance of the Flask class called "app"

#ADD CODE HERE
@app.route('/<int:x>/<int:y>/<color1>/<color2>')          # The "@" decorator associates this route with the function immediately following
def play(x, y, color1, color2):
    return render_template("index.html", row = x, column = y, color1 = color1, color2 = color2) 


    # app.run(debug=True) should be the very last statement! 
if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.