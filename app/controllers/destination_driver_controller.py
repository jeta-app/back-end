from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.destination_driver import Destination_Driver
from app.models.user import Users, Role
from sqlalchemy.exc import SQLAlchemyError

destination_driver_bp = Blueprint('destination_driver_bp', __name__)

@destination_driver_bp.route('/update_destination', methods=['POST'])
@jwt_required()
def update_destination():
    try:
        data = request.json

        if not data or 'destinations' not in data or 'driver_id' not in data:
            return jsonify(message="Invalid JSON format or missing 'destinations' or 'driver_id' field"), 400

        destinations = data.get('destinations')
        driver_id = data.get('driver_id')
        
        if not driver_id or not destinations or not isinstance(destinations, list):
            return jsonify(message="Missing required fields or 'destinations' is not a list"), 400

        for destination in destinations:
            try:
                lat, lng = map(float, destination.split(','))

            except ValueError:
                return jsonify(message="Invalid destination format, each destination must be a string in the format 'lat,lng'"), 400

            existing_destination = Destination_Driver.query.filter_by(driver_id=driver_id, destination_lat=lat, destination_lng=lng).first()

            if existing_destination:
                
                existing_destination.destination_lat = lat
                existing_destination.destination_lng = lng
            else:
                
                new_destination = Destination_Driver(
                    driver_id=driver_id,
                    destination_lat=lat,
                    destination_lng=lng
                )
                db.session.add(new_destination)
        
        db.session.commit()
        return jsonify(message="Destinations updated successfully"), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Failed to update destinations: {str(e)}"), 500



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
