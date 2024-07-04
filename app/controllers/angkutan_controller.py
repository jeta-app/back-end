from flask import jsonify, request, Blueprint
from app.models.location_drivers import Location_Drivers
from app.models.user import Users, Role
from app.models.angkutan import Angkutan
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

angkutan_bp = Blueprint('angkutan', __name__)


@angkutan_bp.route('/angkutan/<int:angkutan_id>', methods=['GET'])
@jwt_required()
def get_angkutan_id(angkutan_id):
    angkutan = Angkutan.query.get(angkutan_id)
    if not angkutan:
        return jsonify(message="Angkutan not found"), 404

    driver_id = angkutan.driver_id
    driver = Users.query.filter_by(id=driver_id, role=Role.Driver).first()

    if not driver:
        return jsonify(message="Driver not found"), 404

    result = {
        'angkutan_id': angkutan.id,
        'angkutan_number': angkutan.angkutan_number,
        'angkutan_jurusan': angkutan.angkutan_jurusan,
        'car_brand': angkutan.car_brand,
        'car_series': angkutan.car_series,
        'driver': {
            'id': driver.id,
            'username': driver.username,
            'firstname': driver.firstname,
            'lastname': driver.lastname,
            'phone_Number': driver.phone_Number,
            'route': driver.route,
            'operational_time': driver.operational_time,
            'status': driver.status.value if driver.status else None
        }
    }
    return jsonify(angkutan=result), 200
