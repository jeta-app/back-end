from flask import jsonify, request, Blueprint
from app.models.location_drivers import Location_Drivers
from app.models.user import Users, Role, Status
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import bcrypt, db

admin_bp = Blueprint('admin', __name__)

def is_admin():
    current_user = get_jwt_identity()
    return current_user['role'] == 'Admin'

@admin_bp.route('/admin/driver', methods=['POST'])
@jwt_required()
def add_driver():
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403
    data = request.get_json()
    required_fields = ['username', 'password', 'email', 'firstname', 'lastname', 'phone_number', 'route', 'operational_time']
    for field in required_fields:
        if field not in data:
            return jsonify(message=f"Missing required field: {field}"), 400

    username = data['username']
    email = data['email']
    password = data['password']
    role = data.get('role', 'Driver')
    firstname = data['firstname']
    lastname = data['lastname']
    phone_number = data['phone_number']
    route = data['route']
    operational_time = data['operational_time']
    status = data.get('status', None)
    angkutan_number = data.get('angkutan_number', None)
    brand_car = data.get('brand_car', None)
    series_car = data.get('series_car', None)

    existing_driver = Users.query.filter_by(username=username).first()
    if existing_driver:
        return jsonify(message="Driver already exists"), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    driver = Users(
        username=username,
        password=hashed_password,
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone_Number=phone_number,
        route=route,
        role=Role.Driver,
        operational_time=operational_time,
        status=status,
        angkutan_number=angkutan_number,
        brand_car=brand_car,
        series_car=series_car,
    )

    db.session.add(driver)
    db.session.commit()
    return jsonify(message="Driver added successfully"), 201

@admin_bp.route('/admin/drivers', methods=['GET'])
@jwt_required()
def get_all_drivers():
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403

    drivers = Users.query.filter_by(role=Role.Driver).all()
    drivers_list = []
    for driver in drivers:
        drivers_list.append({
            'id': driver.id,
            'username': driver.username,
            'firstname': driver.firstname,
            'lastname': driver.lastname,
            'email': driver.email,
            'phone_number': driver.phone_Number,
            'route': driver.route,
            'operational_time': driver.operational_time,
            'status': driver.status.name if driver.status else None,
            'angkutan_number': driver.angkutan_number,
            'brand_car': driver.brand_car,
            'series_car': driver.series_car
        })
    return jsonify(drivers=drivers_list), 200

@admin_bp.route('/admin/driver/<int:driver_id>', methods=['PUT'])
@jwt_required()
def update_driver(driver_id):
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403

    data = request.get_json()
    driver = Users.query.get(driver_id)
    if not driver:
        return jsonify(message="Driver not found"), 404

    if driver.role != Role.Driver:
        return jsonify(message="Can only update users with role 'Driver'"), 403

    if 'username' in data:
        driver.username = data['username']
    if 'email' in data:
        driver.email = data['email']
    if 'phone_number' in data:
        driver.phone_Number = data['phone_number']
    if 'route' in data:
        driver.route = data['route']
    if 'operational_time' in data:
        driver.operational_time = data['operational_time']
    if 'status' in data:
        driver.status = data['status']
    if 'angkutan_number' in data:
        driver.angkutan_number = data['angkutan_number']
    if 'brand_car' in data:
        driver.brand_car = data['brand_car']
    if 'series_car' in data:
        driver.series_car = data['series_car']
        
    db.session.commit()
    return jsonify(message="Driver updated successfully"), 200


@admin_bp.route('/admin/driver/<int:driver_id>', methods=['DELETE'])
@jwt_required()
def delete_driver(driver_id):
    if not is_admin():
        return jsonify(message="Admin privileges required"), 403

    driver = Users.query.get(driver_id)
    if not driver:
        return jsonify(message="Driver not found"), 404

    if driver.role != Role.Driver:
        return jsonify(message="Can only delete users with role 'Driver'"), 403

    db.session.delete(driver)
    db.session.commit()
    return jsonify(message="Driver deleted successfully"), 200
