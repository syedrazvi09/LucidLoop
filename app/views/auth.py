from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')


    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400
    
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'Username or email already exists'}), 400
    
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    