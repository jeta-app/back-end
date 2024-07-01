from flask import jsonify, request, Blueprint
from app.models.location_drivers import Location_Drivers
from app.models.user import Users
from app.models.angkutan import Angkutan
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

admin_bp = Blueprint('admin', __name__)

def is_admin():
    current_user = get_jwt_identity()
    print(current_user)
    print(current_user['Role'])
    return current_user['Role'] == 'Admin'

@admin_bp.route('/angkutan',methods=['POST'])
@jwt_required()
def add_angkutan():
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403   
    data = request.get_json()
    if not data or 'pat' not in data or 'driver_id' not in data or 'angkutan_jurusan' not in data:
        return jsonify(message="Missing required fields"), 400
    angkutan_number = data['angkutan_number']
    angkutan_jurusan = data['angkutan_jurusan']
    driver_id = data['driver_id']
    existing_angkutan = Angkutan.query.filter_by(Angkutan_Number=angkutan_number).first()
    if existing_angkutan:
        return jsonify(message="Angkutan number already exists"), 400
    driver = User.query.filter_by(User_id=driver_id, Role=Role.Driver).first()
    if not driver:
        return jsonify(message="Driver not found or invalid role"), 400
    angkutan = Angkutan(Angkutan_Number=angkutan_number, Angkutan_Jurusan=angkutan_jurusan, Driver_ID=driver_id)
    db.session.add(angkutan)
    db.session.commit()
    return jsonify(message="Angkutan added successfully", angkutan_id=angkutan.Angkutan_ID), 201

@admin_bp.route('/angkutan', methods=['GET'])
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

@admin_bp.route('/angkutan/<int:angkutan_id>', methods=['GET'])
@jwt_required()
def get_angkutan_id(angkutan_id):
    angkutan = Angkutan.query.get(angkutan_id)
    if not angkutan:
        return jsonify(message="Angkutan not found"), 404
    result = {
        'angkutan_id': angkutan.Angkutan_ID,
        'angkutan_number': angkutan.Angkutan_Number,
        'angkutan_jurusan': angkutan.Angkutan_Jurusan,
        'driver_id': angkutan.Driver_ID,
    }
    return jsonify(angkutan=result), 200

@admin_bp.route('/angkutan/<int:angkutan_id>', methods=['PUT'])
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
        driver = User.query.filter_by(User_id=driver_id, Role=Role.Driver).first()
        if not driver:
            return jsonify(message="Driver not found or invalid role"), 400
        angkutan.Driver_ID = driver_id

    db.session.commit()
    return jsonify(message="Bus updated successfully"), 200

@admin_bp.route('/angkutan/<int:angkutan_id>', methods=['DELETE'])
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