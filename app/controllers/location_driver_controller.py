# app/controllers/locationupdate_controller.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db, socketio
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

    # Cari atau buat entri Location_Drivers berdasarkan driver_id
    location_driver = Location_Drivers.query.filter_by(driver_id=driver_id).first()
    if location_driver:
        # Update data lokasi
        location_driver.origin_lat = origin['lat']
        location_driver.origin_lng = origin['lng']
        location_driver.destination_lat = destination['lat']
        location_driver.destination_lng = destination['lng']
        location_driver.heading = heading
    else:
        # Buat entri baru jika tidak ada
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

    # Emit acara locationUpdate ke semua klien yang terhubung
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

    location_driver = Location_Drivers.query.filter_by(driver_id=driver_id).first()
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





























