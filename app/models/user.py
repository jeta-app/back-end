from app import db
from enum import Enum


class Role(Enum):
    Admin = 'Admin'
    Driver = 'Driver'
    Passenger = 'Passenger'


class Status(Enum):
    Active = "Active"
    Inactive = "Inactive"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(200), nullable=False)
    phone_Number = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    route = db.Column(db.String(200), nullable=True)
    operational_time = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Enum(Status), nullable=True)

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.role != Role.Driver:
            self.route = None
            self.operational_time = None
            self.status = None
