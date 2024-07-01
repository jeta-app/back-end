from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.models.location_drivers import Location_Drivers
from app.models.user import Users, Role
from app.models.angkutan import Angkutan
from app import db,bcrypt,jwt

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    fields_required = ['username', 'password', 'firstname', 'lastname', 'email', 'phone']
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
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = Users.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        print(user.role)
        access_token = create_access_token(identity={'id': user.id,'username': username, 'role': user.role.name})
    return jsonify(access_token=access_token), 200

