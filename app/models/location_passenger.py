# app/models/location_passenger.py

from app import db

class LocationPassenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, nullable=False)  # ID penumpang
    lat = db.Column(db.Float, nullable=False)  # Latitude
    lng = db.Column(db.Float, nullable=False)  # Longitude
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.current_timestamp())
