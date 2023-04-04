from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/CollegeInventory'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

app.app_context().push()

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwdhash = db.Column(db.String(128), nullable=False)
    teachers = db.relationship('Teacher', backref='user', lazy=True)
    students = db.relationship('Student', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        print('setting password...')
        self.pwdhash = generate_password_hash(password)

    def verify_password(self, password):
        print('checking password...')
        return check_password_hash(self.pwdhash, password)
    
    def __repr__(self):
        return f"User: {self.name}"
    
    def __init__(self, username, type, email):
        self.username = username
        self.type = type
        self.email = email 

class Teacher(db.Model):
    __tablename__ = 'teacher'
    tid = db.Column(db.Integer, db.ForeignKey('user.userid'), primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    dept = db.Column(db.String, nullable=False)
    qualification = db.Column(db.String, nullable=False)
    institute = db.Column(db.String, nullable=False)
    linkedin_url = db.Column(db.String, nullable=False)
    students = db.relationship('Student', backref='teacher', lazy=True)

    def __repr__(self):
        return f"Teacher: {self.fname}"
    
    def __init__(self, fname, lname, dept, qualification, institute, linkedin_url):
        self.fname = fname
        self.lname = lname
        self.dept = dept
        self.qualification = qualification
        self.institute = institute
        self.linkedin_url = linkedin_url 

class Student(db.Model):
    __tablename__ = 'student'
    sid = db.Column(db.Integer, db.ForeignKey('user.userid'), primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    year_admitted = db.Column(db.Integer, nullable=False)
    institute = db.Column(db.String, nullable=False)
    enrollment_id = db.Column(db.String, unique=True, nullable=False)
    linkedin_url = db.Column(db.String, nullable=False)
    tid = db.Column(db.Integer, db.ForeignKey('teacher.tid'), nullable=False)
    certificates = db.relationship('Certificate', backref='student', lazy=True)

    def __repr__(self):
        return f"Student: {self.fname}"
    
    def __init__(self, fname, lname, year_admitted, institute, enrollment_id, linkedin_url):
        self.fname = fname
        self.lname = lname
        self.year_admitted = year_admitted
        self.enrollment_id = enrollment_id
        self.institute = institute
        self.linkedin_url = linkedin_url 

class Certificate(db.Model):
    __tablename__ = 'certificate'
    certid = db.Column(db.Integer, primary_key=True, autoincrement = True)
    sid = db.Column(db.Integer, db.ForeignKey('student.sid'), nullable=False)
    certname = db.Column(db.String, nullable=False)
    domain = db.Column(db.String, nullable=False)
    issued_by = db.Column(db.String, nullable=False)
    issued_on = db.Column(db.Date, nullable=False)
    validity = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Certificate: {self.certname}"
    
    def __init__(self, certname, domain, issued_by, issued_on, validity):
        self.certname = certname 
        self.domain = domain
        self.issued_by = issued_by
        self.issued_on = issued_on
        self.validity = validity

class Tag(db.Model):
    __tablename__ = 'tag'
    tagid = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String, unique=True, nullable=False)
    type = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Tag: {self.name}"
    
    def __init__(self, name, type):
        self.name = name 
        self.type = type
    

@app.route("/")
def hello():
    return "hi"

if __name__ == '__main__':
    app.run()