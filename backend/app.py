from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/CollegeInventory'
db = SQLAlchemy(app) 

class Student(db.Model):
    pass

class Teacher(db.Model):
    pass

@app.route("/")
def hello():
    return "hi"

if __name__ == '__main__':
    app.run()