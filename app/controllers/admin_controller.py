from flask import jsonify, request, Blueprint
from app.models.location_drivers import Location_Drivers
from app.models.user import Users, Role
from app.models.angkutan import Angkutan
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

admin_bp = Blueprint('admin', __name__)


def is_admin():
    current_user = get_jwt_identity()
    print(current_user)
    print(current_user['role'])
    return current_user['role'] == 'Admin'


@admin_bp.route('/admin/angkutan', methods=['POST'])
@jwt_required()
def add_angkutan():
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403
    data = request.get_json()
    if not data or 'driver_id' not in data or 'angkutan_jurusan' not in data:
        return jsonify(message="Missing required fields"), 400
    angkutan_number = data['angkutan_number']
    angkutan_jurusan = data['angkutan_jurusan']
    driver_id = data['driver_id']
    car_brand = data['car_brand']
    car_series = data['car_series']
    existing_angkutan = Angkutan.query.filter_by(
        angkutan_number=angkutan_number).first()
    if existing_angkutan:
        return jsonify(message="Angkutan number already exists"), 400
    driver = Users.query.filter_by(
        id=driver_id, role=Role.Driver).first()
    if not driver:
        return jsonify(message="Driver not found or invalid role"), 400
    angkutan = Angkutan(angkutan_number=angkutan_number,
                        angkutan_jurusan=angkutan_jurusan, driver_id=driver_id, car_brand=car_brand, car_series=car_series)
    db.session.add(angkutan)
    db.session.commit()
    return jsonify(message="Angkutan added successfully", angkutan_id=angkutan.id), 201


@admin_bp.route('/admin/angkutan', methods=['GET'])
@jwt_required()
def get_angkutan():
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403
    angkutan = Angkutan.query.all()
    hasil = []
    for angkutans in angkutan:
        hasil.append({
            'angkutans_jurusan': angkutans.Angkutan_ID,
            'angkutans_jurusan': angkutans.Angkutan_Name,
            'driver_id': angkutans.Driver_ID,
        })
    return jsonify(angkutan=result), 200


@admin_bp.route('/admin/angkutan/<int:angkutan_id>', methods=['PUT'])
@jwt_required()
def update_angkutan(angkutan_id):
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403
    data = request.get_json()
    angkutan = Angkutan.query.get(angkutan_id)
    if not angkutan:
        return jsonify(message="Angkutan not found"), 404
    if 'angkutan_number' in data:
        angkutan.Angkutan_Number = data['angkutan_number']
    if 'driver_id' in data:
        driver_id = data['driver_id']
        driver = User.query.filter_by(
            User_id=driver_id, Role=Role.Driver).first()
        if not driver:
            return jsonify(message="Driver not found or invalid role"), 400
        angkutan.Driver_ID = driver_id

    db.session.commit()
    return jsonify(message="Bus updated successfully"), 200


@admin_bp.route('/admin/angkutan/<int:angkutan_id>', methods=['DELETE'])
@jwt_required()
def delete_angkutan(angkutan_id):
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403

    angkutan = Angkutan.query.get(bus_id)
    if not bus:
        return jsonify(message="Bus not found"), 404

    db.session.delete(angkutan)
    db.session.commit()
    return jsonify(message="Angkutan deleted successfully"), 200
