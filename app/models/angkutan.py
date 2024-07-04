
from app import db
from app.models.user import Users


class Angkutan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angkutan_number = db.Column(db.String(20), nullable=False)
    angkutan_jurusan = db.Column(db.String(150), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    car_brand = db.Column(db.String(100), nullable=False)
    car_series = db.Column(db.String(100), nullable=False)
