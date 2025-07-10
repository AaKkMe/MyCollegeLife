# Import the tools
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__,template_folder='../Frontend')

# This line alllows the frontend on a different address to make request to our backend
CORS(app)

#Configuring database
#This tells our app where to find the database file. We're calling it database.b
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #optionsel feature truning off to save memory

#step 3:
db = SQLAlchemy(app) #object of database
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
