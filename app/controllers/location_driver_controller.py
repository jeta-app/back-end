from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, socketio
from flask_socketio import SocketIO, emit
from app.models.user import Users, Role
from app.models.location_drivers import Location_Drivers

location_bp = Blueprint('location_update', __name__)


@location_bp.route('/update', methods=['POST'])
@jwt_required()
def update_location():
    data = request.json
    if not data:
        return jsonify(message="Invalid JSON format"), 400

    driver_id = data.get('driver_id')
    origin = data.get('origin')
    destination = data.get('destination')
    heading = data.get('heading', 0)

    if not driver_id or not origin or not destination:
        return jsonify(message="Missing required fields"), 400
    location_driver = Location_Drivers.query.filter_by(
        driver_id=driver_id).first()
    if location_driver:
        location_driver.origin_lat = origin['lat']
        location_driver.origin_lng = origin['lng']
        location_driver.destination_lat = destination['lat']
        location_driver.destination_lng = destination['lng']
        location_driver.heading = heading
    else:
        location_driver = Location_Drivers(
            driver_id=driver_id,
            origin_lat=origin['lat'],
            origin_lng=origin['lng'],
            destination_lat=destination['lat'],
            destination_lng=destination['lng'],
            heading=heading
        )
        db.session.add(location_driver)

    db.session.commit()
    socketio.emit('locationUpdate', {
        'driver_id': driver_id,
        'origin': origin,
        'destination': destination,
        'heading': heading
    })

    return jsonify(message="Location updated successfully"), 200


@socketio.on('locationUpdate')
def handle_update_location(data):
    print(data)
    if not data:
        return False, {'message': "Invalid JSON format"}
    driver_id = data.get('driver_id')
    origin = data.get('origin')
    destination = data.get('destination')
    heading = data.get('heading', 0)

    if not driver_id or not origin or not destination:
        return False, {'message': "Missing required fields"}

    location_driver = Location_Drivers.query.filter_by(
        driver_id=driver_id).first()
    if location_driver:
        location_driver.origin_lat = origin['lat']
        location_driver.origin_lng = origin['lng']
        location_driver.destination_lat = destination['lat']
        location_driver.destination_lng = destination['lng']
        location_driver.heading = heading
    else:
        location_driver = Location_Drivers(
            driver_id=driver_id,
            origin_lat=origin['lat'],
            origin_lng=origin['lng'],
            destination_lat=destination['lat'],
            destination_lng=destination['lng'],
            heading=heading
        )
        db.session.add(location_driver)

    db.session.commit()
    socketio.emit('locationUpdate', {
        'driver_id': driver_id,
        'origin': origin,
        'destination': destination,
        'heading': heading
    })

    return True, {'message': "Location updated successfully"}


@location_bp.route('/all_driver_locations', methods=['GET'])
@jwt_required()
def get_all_driver_locations():
    locations = Location_Drivers.query.all()
    location_data = [{
        'driver_id': loc.driver_id,
        'origin': {'lat': loc.origin_lat, 'lng': loc.origin_lng},
        'destination': {'lat': loc.destination_lat, 'lng': loc.destination_lng},
        'heading': loc.heading
    } for loc in locations]

    return jsonify(location_data), 200


@socketio.on('requestAllDriverLocations')
def handle_all_driver_locations(data):
    locations = Location_Drivers.query.all()
    location_data = [{
        'driver_id': loc.driver_id,
        'origin': {'lat': loc.origin_lat, 'lng': loc.origin_lng},
        'destination': {'lat': loc.destination_lat, 'lng': loc.destination_lng},
        'heading': loc.heading
    } for loc in locations]

    emit('allDriverLocations', location_data)


@socketio.on('allDriversUpdate')
def handle_available_drivers_update(data):
    available_drivers = Users.query.filter_by(role=Role.Driver.name).all()
    drivers_data = [{
        'id': driver.id,
        'username': driver.username,
        'email': driver.email,
        'firstname': driver.firstname,
        'lastname': driver.lastname,
        'phone_Number': driver.phone_Number,
        'route': driver.route,
        'operational_time': driver.operational_time
    } for driver in available_drivers]

    emit('allDriversUpdate', drivers_data, broadcast=True)
    print('Sent available drivers update to connected clients')
