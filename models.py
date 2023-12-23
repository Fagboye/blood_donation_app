from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_utils import ChoiceType


db = SQLAlchemy()


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
