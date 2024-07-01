from app import db
from enum import Enum

class Role(Enum):
    Admin = 'Admin'
    Driver = 'Driver'
    Passenger = 'Passenger'

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    phone_Number = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)