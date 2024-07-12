from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.destination_driver import Destination_Driver
from app.models.user import Users, Role

destination_driver_bp = Blueprint('destination_driver_bp', __name__)

@destination_driver_bp.route('/update_destination', methods=['POST'])
@jwt_required()
def update_destination():
    try:
        data = request.json

        if not data or 'destination' not in data:
            return jsonify(message="Invalid JSON format or missing 'destination' field"), 400

        destination = data.get('destination')
        driver_id = data.get('driver_id')
        
        if not driver_id or not destination:
            return jsonify(message="Missing required fields"), 400

        destination_driver = Destination_Driver.query.filter_by(
        driver_id=driver_id).first()

        if destination_driver:
            destination_driver.destination_lat = destination['lat']
            destination_driver.destination_lng = destination['lng']
        else:
            destination_driver = Destination_Driver(
                driver_id=driver_id,
                destination_lat=destination['lat'],
                destination_lng=destination['lng']
            )
            db.session.add(destination_driver)

        db.session.commit()
        return jsonify(message="Destination updated successfully"), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Failed to update destination: {str(e)}"), 500

@destination_driver_bp.route('/all_destinations', methods=['GET'])
@jwt_required()
def get_all_destinations():
    try:
        destination_drivers = Destination_Driver.query.all()

        destinations = [
            {
                'driver_id': driver.driver_id,
                'destination': {
                    'lat': driver.destination_lat,
                    'lng': driver.destination_lng
                }
            }
            for driver in destination_drivers
        ]

        return jsonify(destinations), 200

    except Exception as e:
        return jsonify(message=f"Failed to retrieve destinations: {str(e)}"), 500
