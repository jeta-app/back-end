from flask import Blueprint, request, jsonify, current_app
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

        if not data or 'destinations' not in data or 'driver_id' not in data or 'origin' not in data:
            return jsonify(message="Invalid JSON format or missing 'destinations', 'driver_id', or 'origin' field"), 400

        destinations = data.get('destinations')
        origin = data.get('origin')
        driver_id = data.get('driver_id')

        if not driver_id or not destinations or not isinstance(destinations, list) or not origin:
            return jsonify(message="Missing required fields or 'destinations' is not a list"), 400

        try:
            origin_lat, origin_lng = map(float, origin.split(','))
        except ValueError:
            return jsonify(message="Invalid origin format, it must be a string in the format 'lat,lng'"), 400

        for destination in destinations:
            try:
                dest_lat, dest_lng = map(float, destination.split(','))
            except ValueError:
                return jsonify(message="Invalid destination format, each destination must be a string in the format 'lat,lng'"), 400

            print(f"Querying DB with Driver ID: {driver_id}, Dest Lat: {dest_lat}, Dest Lng: {dest_lng}")

            existing_destination = Destination_Driver.query.filter(
                Destination_Driver.driver_id == driver_id,
                db.func.abs(Destination_Driver.destination_lat - dest_lat) < 0.0001,
                db.func.abs(Destination_Driver.destination_lng - dest_lng) < 0.0001
            ).first()

            if existing_destination:
                existing_destination.origin_lat = origin_lat
                existing_destination.origin_lng = origin_lng
            else:
                new_destination = Destination_Driver(
                    driver_id=driver_id,
                    destination_lat=dest_lat,
                    destination_lng=dest_lng,
                    origin_lat=origin_lat,
                    origin_lng=origin_lng
                )
                db.session.add(new_destination)

        db.session.commit()
        return jsonify(message="Destinations updated or created successfully"), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Failed to update or create destinations: {str(e)}"), 500



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
