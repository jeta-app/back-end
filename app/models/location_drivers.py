
from app import db

class Location_Drivers(db.Model):
    __tablename__ = 'location_drivers'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    origin_lat = db.Column(db.Float, nullable=False)
    origin_lng = db.Column(db.Float, nullable=False)
    heading = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())