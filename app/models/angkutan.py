
from app import db
from app.models.user import Users

class Angkutan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Angkutan_Number = db.Column(db.String(20), nullable=False)
    jurusan = db.Column(db.String(150), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    driver = db.relationship('Users', backref=db.backref('angkutan', lazy=True))