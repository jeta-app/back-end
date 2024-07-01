from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, socketio
from app.models.user import Users, Role
from app.models.location_passenger import LocationPassenger

location_passenger_bp = Blueprint('location', __name__)

@location_passenger_bp.route('/share-location', methods=['POST'])
@jwt_required()
def share_location():
    current_user = get_jwt_identity()

    # Mengambil ID pengguna dari JWT
    current_passenger_id = current_user.get('id')
    role = current_user.get('role')

    if not current_passenger_id:
        return jsonify(message="User ID not found in JWT"), 400

    # Pastikan hanya pengguna dengan peran "Passenger" yang dapat berbagi lokasi
    if role != Role.Passenger.name:
        return jsonify(message="Only passengers can share location"), 403

    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')

    if not lat or not lng:
        return jsonify(message="Latitude and longitude are required"), 400

    # Cari atau buat entri Location_Passenger berdasarkan passenger_id
    location_passenger = LocationPassenger.query.filter_by(passenger_id=current_passenger_id).first()

    if not location_passenger:
        location_passenger = LocationPassenger(
            passenger_id=current_passenger_id,
            lat=lat,
            lng=lng
        )
        db.session.add(location_passenger)
    else:
        location_passenger.lat = lat
        location_passenger.lng = lng

    db.session.commit()

    # Emit event 'locationUpdate' kepada semua klien terhubung
    socketio.emit('locationUpdate', {
        'passenger_id': current_passenger_id,
        'lat': lat,
        'lng': lng
    })

    return jsonify(message="Location shared successfully"), 200
