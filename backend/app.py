from flask import Flask, jsonify, request
import os, random, string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json
from functools import wraps
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
# from config import BaseConfig

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY', None)
if not app.config["SECRET_KEY"]:
    app.config["SECRET_KEY"] = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY', None)
if not app.config["JWT_SECRET_KEY"]:
    app.config["JWT_SECRET_KEY"] = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost/CollegeInventory'

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

app.app_context().push()

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
        return f"User: {self.username}"
    
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

@app.route("/home")
def hello():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

@app.route('/token', methods=["POST"])
def create_token():
    print(request.is_json)
    data = request.get_json()
    # print(data)
    # print(type(data))
    # return data
    # print(json.dumps(data))
    # return json.dumps(data)
    # print(data)
    email = data["email"]
    password = data["password"]
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response

# def token_required(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         token = None
#         if "authorization" in request.headers:
#             token = request.headers["authorization"]
#         if not token:
#             return {"success": False, "msg": "Valid JWT token is missing"}, 400
#         try:
#             data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=["HS256"])
#             current_user = User.get_by_email(data["email"])
#             if not current_user:
#                 return {"success": False,
#                         "msg": "Sorry. Wrong auth token. This user does not exist."}, 400
#             token_expired = db.session.query(JWTTokenBlocklist.id).filter_by(jwt_token=token).scalar()
#             if token_expired is not None:
#                 return {"success": False, "msg": "Token revoked."}, 400
#             if not current_user.check_jwt_auth_active():
#                 return {"success": False, "msg": "Token expired."}, 400
#         except:
#             return {"success": False, "msg": "Token is invalid"}, 400
#         return f(current_user, *args, **kwargs)
#     return decorator

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        req_data = request.get_json()

        username = req_data.get("username")
        email = req_data.get("email")
        type = req_data.get("type")
        pwd = req_data.get("pwd")
        cnfpwd = req_data.get("cnfpwd")

        if pwd != cnfpwd:
            return {"success": False, 
                    "msg": "Passwords do not match"}, 400

        user_exists = User.get_by_email(email)
        if user_exists:
            return {"success": False,
                    "msg": "Email already taken"}, 400
        
        if type not in ['student', 'teacher']:
            return {"success": False,
                    "msg": "User can only be a teacher or a student"}, 400

        new_user = User(username=username, email=email, type=type)
        new_user.set_password(pwd)

        new_user.save()

        return {"success": True,
                "userid": new_user.userid,
                "msg": "The user was successfully registered"}, 200


@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    email = req_data.get("email")
    password = req_data.get("pwd")

    user_exists = User.get_by_email(email)
    print(user_exists)
    if not user_exists:
        return {"success": False,
                "msg": "User does not exist"}, 400
    
    if not user_exists.check_password(password):
            return {"success": False,
                    "msg": "Invalid credentials"}, 400
    
    token = create_access_token(identity=email)
    user_exists.set_jwt_auth_active(True)
    user_exists.save()

    return {"success": True,
            "token": token,
            "user": user_exists.toJSON()}, 200


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# @app.route('/updateStudent', methods=['POST','GET'])
# @jwt_required
# def updateS(self):
#     if request.method == 'POST':
#         req_data = request.get_json()

#         fname = req_data.get("fname")
#         lname = req_data.get("lname")
#         year_admitted = req_data.get("year_admitted")
#         institute = req_data.get("institute")
#         enrollment_id = req_data.get("enrollment_id")
#         linkedin_url = req_data.get("linkedin_url")

#         if not fname or not lname or not year_admitted or not institute or not enrollment_id or not linkedin_url:
#             return {"success": False,
#                     "msg": "Invalid input"}, 400
        
        

#     else:

if __name__ == '__main__':
    app.run()