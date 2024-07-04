from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, socketio
from flask_socketio import SocketIO, emit
from app.models.user import Users, Role
from app.models.location_passenger import LocationPassenger
import json
location_passenger_bp = Blueprint('location', __name__)


@location_passenger_bp.route('/share-location', methods=['POST'])
@jwt_required()
def share_location():
    current_user = get_jwt_identity()
    current_passenger_id = current_user.get('id')
    role = current_user.get('role')

    if not current_passenger_id:
        return jsonify(message="User ID not found in JWT"), 400
    if role != Role.Passenger.name:
        return jsonify(message="Only passengers can share location"), 403

    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')

    if not lat or not lng:
        return jsonify(message="Latitude and longitude are required"), 400

    location_passenger = LocationPassenger.query.filter_by(
        passenger_id=current_passenger_id).first()

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
    socketio.emit('passengerLocationUpdate', {
        'passenger_id': current_passenger_id,
        'lat': lat,
        'lng': lng,
        'timestamp': location_passenger.timestamp.isoformat()
    }, broadcast=True)

    return jsonify(message="Location shared successfully"), 200


@location_passenger_bp.route('/getallpassengers', methods=['GET'])
@jwt_required()
def get_all_passengers():
    current_user = get_jwt_identity()
    if current_user.get('role') != Role.Driver.name:
        return jsonify(message="Only passanger can access active drivers"), 403
    active_passengers = LocationPassenger.query.all()
    passengers_data = [{
        'passenger_id': passenger.passenger_id,
        'lat': passenger.lat,
        'lng': passenger.lng,
        'timestamp': passenger.timestamp.isoformat()
    } for passenger in active_passengers]

    return jsonify(passengers_data), 200


@socketio.on('requestAllPassengerLocations')
def handle_all_passenger_locations(data):
    active_passengers = LocationPassenger.query.all()
    passenger_data = [{
        'passenger_id': passenger.passenger_id,
        'lat': passenger.lat,
        'lng': passenger.lng,
        'timestamp': passenger.timestamp.isoformat()
    } for passenger in active_passengers]

    emit('allPassengerLocations', passenger_data)


@socketio.on('passengerLocationUpdate')
def handle_passenger_location_update(data):
    passenger_id = data.get('passenger_id')
    lat = data.get('lat')
    lng = data.get('lng')

    if not passenger_id or not lat or not lng:
        return

    location_passenger = LocationPassenger.query.filter_by(
        passenger_id=passenger_id).first()
    if location_passenger:
        location_passenger.lat = lat
        location_passenger.lng = lng
        db.session.commit()
    else:
        location_passenger = LocationPassenger(
            passenger_id=passenger_id,
            lat=lat,
            lng=lng
        )
        db.session.add(location_passenger)
        db.session.commit()

    emit('passengerLocationUpdate', {
        'passenger_id': passenger_id,
        'lat': lat,
        'lng': lng,
        'timestamp': location_passenger.timestamp.isoformat()
    }, broadcast=True)
