from app import db
from app.models.user import Users
class Destination_Driver(db.Model):
    __tablename__ = 'destination_driver'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    destination_lat = db.Column(db.Double, nullable=False)
    destination_lng = db.Column(db.Double, nullable=False)
    origin_lat = db.Column(db.Double, nullable=False)
    origin_lng = db.Column(db.Double, nullable=False)

