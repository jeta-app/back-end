from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.models.location_drivers import Location_Drivers
from app.models.user import Users, Role, Status
from app.models.angkutan import Angkutan
from app import db, bcrypt, jwt

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    fields_required = ['username', 'password',
                       'firstname', 'lastname', 'email', 'phone']
    if not data or not all(field in data for field in fields_required):
        return jsonify(message="Missing required fields"), 400
    username = data['username']
    password = data['password']
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    phone = data['phone']
    role = data.get('role', 'Passenger')
    if Users.query.filter_by(username=username).first():
        return jsonify(message="User already registered"), 400
    try:
        user_role = Role[role.capitalize()]
    except KeyError:
        return jsonify(message="Invalid role"), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = Users(
        username=username,
        password=hashed_password,
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone_Number=phone,
        role=user_role
    )
    if user_role == Role.Driver:
        route = data.get('route')
        operational_time = data.get('operational_time')
        if not route or not operational_time:
            return jsonify(message="Driver role requires route and operational_time"), 400
        user.route = route
        user.operational_time = operational_time

    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = Users.query.filter_by(username=username).first()

    if not user:
        return jsonify(message="User not found"), 404

    if bcrypt.check_password_hash(user.password, password):
        # Set driver status to active if the user is a driver
        if user.role == Role.Driver:
            user.status = Status.Active
            db.session.commit()

        access_token = create_access_token(
            identity={'id': user.id, 'username': username,
                      'role': user.role.name}
        )
        return jsonify(access_token=access_token), 200

    return jsonify(message="Invalid credentials"), 401


@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    user = Users.query.get(current_user['id'])

    if user and user.role == Role.Driver:
        user.status = Status.Inactive
        db.session.commit()

    return jsonify(message="Successfully logged out"), 200


@jwt.expired_token_loader
def expired_token_callback(expired_token, decoded_token):
    token_type = decoded_token['type']
    identity = decoded_token['sub']

    if token_type == 'access':
        user_id = identity['id']
        user = Users.query.get(user_id)
        if user and user.role == Role.Driver:
            user.status = Status.Inactive
            db.session.commit()

    return jsonify({
        'message': 'The token has expired',
        'error': 'token_expired'
    }), 401


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()

    user_id = current_user['id']  # Ambil id pengguna dari token JWT
    user = Users.query.get(user_id)

    if not user:
        return jsonify(message="User not found"), 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'phone_number': user.phone_Number,
        'role': user.role.name,
        'route': user.route,
        'operational_time': user.operational_time
    }

    return jsonify(user=user_data), 200
