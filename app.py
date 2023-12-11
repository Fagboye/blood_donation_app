from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType
from datetime import datetime
import bcrypt
import jwt
from sqlalchemy import desc
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)



# DEFINING THE TABLES IN THE DATABASE

# the user model 
class User(db.Model):
  Gender_choices = [
      ('male', "Male"),
      ('female', "Female"),
  ]
  BLOOD_GROUP_CHOICES = [
       ('A+', 'A+'),
       ('A-', 'A-'),
       ('B+', 'B+'),
       ('B-', 'B-'),
       ('AB+', 'AB+'),
       ('AB-', 'AB-'),
       ('O+', 'O+'),
       ('O-', 'O-')
   ]
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(200), nullable=False)
  first_name = db.Column(db.String(80), nullable=False)
  last_name = db.Column(db.String(80), nullable=False)
  gender = db.Column(ChoiceType(Gender_choices), nullable=False)
  blood_group = db.Column(ChoiceType(BLOOD_GROUP_CHOICES), nullable=False)

# the donation log model 
class DonationLog(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# the schedule table 
class Schedulelog(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   schedule_date = db.Column(db.DateTime, nullable=False)

with app.app_context():
  db.create_all()

# import the secret token from the .env file 
load_dotenv()


# define the generate_token function 
def generate_token(user_id):
  #define the payload for the token 
  payload = {'user_id': user_id}

  # generate the token 
  token = jwt.encode(payload, os.getenv("SECRET_TOKEN"), algorithm='HS256')

  #return the token as a string
  return token


@app.route('/')
def index():
  return 'Hello from Flask!'

@app.route('/register', methods=['POST'])
def register():
  # extract the user registration data from the request
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  first_name = data.get('first_name')
  last_name = data.get('last_name')
  gender = data.get('gender')
  blood_group = data.get('blood_group')

  existing_user = User.query.filter_by(username=username).first()
  if existing_user is not None:
    return jsonify({'error': 'Username already exists'}), 400

  # Hash the password 
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  #create a user
  user = User(username=username, password=hashed_password, first_name=first_name, last_name=last_name, gender=gender, blood_group=blood_group)

  # save the user to the database 
  db.session.add(user)
  db.session.commit()

  gender = user.gender.code
  blood_group = user.blood_group.code

  #return a response
  return jsonify({
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'gender': gender,
        'blood_group': blood_group
    })

# FUNCTION TO CHECK THE AUTHORIZATION OF THE USER WHEN INTERACTING WITH THE DATABASE
def get_user_id_from_token(token):
       try:
           payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
           user_id = payload['user_id']
           return user_id
       except jwt.ExpiredSignatureError:
           return None
       except jwt.InvalidTokenError:
           return None


# LOGIN ROUTE AND FUNCTION
@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    # extract the login data from the request 
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # retrieve the user from the database
    user = User.query.filter_by(username=username).first()

    # verify the user password 
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
      #generate and return an authetnication token 
      token = generate_token(user.id)
      return jsonify({'token': token, })
    else:
      return jsonify({"error": 'Invalid username or password'})
    
  # TO RETRIEVE USER INFORMATION 
  elif request.method == 'GET':
    user_id = get_user_id_from_token(request.headers.get('Authorization'))

    if user_id is None:
      return jsonify({'error': 'invalid or expired authorization token'}), 401
    
    # retrieve the user information from the database
    user = User.query.get(user_id)

    # retrieve the user's last donation date from the database, I THINK THERE WILL BE BETTER WAY TO DO THIS THOUGH 
    last_donation = DonationLog.query.filter_by(user_id=user_id).order_by(desc(DonationLog.date)).first()

    gender = user.gender.code
    blood_group = user.blood_group.code  

  # returns the user's information as a response of the view 
    return jsonify({
          'id': user.id,
          'username': user.username,
          'first_name': user.first_name,
          'last_name': user.last_name,
          'gender': gender,
          'blood_group': blood_group,
          'last_donation': last_donation
      })

       



# ROUTE AND VIEW TO SCHEDUELE AN APPIONTMENT FOR A BLOOD DONATION 
@app.route('/schedule', methods=['POST', "GET"])
def schedule_appointment():
   if request.method == "POST":
    user_id = get_user_id_from_token(request.headers.get('Authorization'))
    if user_id is None:
        return jsonify({'error': 'Invalid or expired authorization token'})
    
    #make a new instance of a schedule in the schedule table of the database 
    schedule_date = request.form.get('schedule_date')
    new_schedule = Schedulelog(user_id=user_id, schedule_date=schedule_date)
    return jsonify({'message': 'schedule successfully made'})
   if request.method == "GET":
        pass





if __name__ == '__main__':
  app.run(debug=True)