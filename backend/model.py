from datetime import datetime
import json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwdhash = db.Column(db.String(128), nullable=False)
    jwt_auth_active = db.Column(db.Boolean())
    teachers = db.relationship('Teacher', backref='user', lazy=True)
    students = db.relationship('Student', backref='user', lazy=True)

    def set_password(self, password):
        print('setting password...')
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        print('checking password...')
        return check_password_hash(self.pwdhash, password)
    
    def check_jwt_auth_active(self):
        return self.jwt_auth_active

    def set_jwt_auth_active(self, set_status):
        self.jwt_auth_active = set_status
    
    def __repr__(self):
        return f"User: {self.name}"
    
    def __init__(self, username, type, email):
        self.username = username
        self.type = type
        self.email = email 

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def toDICT(self):
        cls_dict = {}
        cls_dict['userid'] = self.userid
        cls_dict['username'] = self.username
        cls_dict['email'] = self.email
        cls_dict['type'] = self.type

        return cls_dict

    def toJSON(self):
        return self.toDICT()

class JWTTokenBlocklist(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jwt_token = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    def __repr__(self):
        return f"Expired Token: {self.jwt_token}"

    def save(self):
        db.session.add(self)
        db.session.commit()

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

    def save(self):
        db.session.add(self)
        db.session.commit()

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

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_year(cls, year):
        return cls.query.filter_by(year_admitted=year)

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

    def save(self):
        db.session.add(self)
        db.session.commit()

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

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()