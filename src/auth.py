from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import User, db
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
import src.constants.http_status_codes as error
import validators
from flasgger import swag_from


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


# REGISTER WITH USERNAME, EMAIL AND PASSWORD
@auth.post("/register")
@swag_from('./docs/register.yaml')
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    # VALIDATIONS OF USER PARAMETERS
    if len(password) < 6:
        return jsonify({"Error": "Password is too short"}), error.HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({"Error": "Username is too short"}), error.HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return (
            jsonify({"error": "Username should be alphanumeric, also no spaces"}),
            error.HTTP_400_BAD_REQUEST,
        )

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), error.HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email is taken"}), error.HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "username is taken"}), error.HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    # ADDING USER TO THE DATABASE
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {"message": "User created", "user": {"username": username, "email": email}}
        ),
        error.HTTP_201_CREATED,
    )


# LOGIN WITH EMAIL AND PASSWORD
@auth.post("/login")
@swag_from('./docs/login.yaml')
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return (
                jsonify(
                    {
                        "user": {
                            "refresh": refresh,
                            "access": access,
                            "username": user.username,
                            "email": user.email,
                        }
                    }
                ),
                error.HTTP_200_OK,
            )

    return jsonify({"error": "Wrong credentials"}), error.HTTP_401_UNAUTHORIZED


# RETURN CURRENT LOGGED USER BY JWT_IDENTITY
@auth.get("/currentUser")
@jwt_required()
def getCurrentUser():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    return jsonify({"username": user.username, "email": user.email}), error.HTTP_200_OK


#REFRESH ACCESS TOKEN USING REFRESH TOKEN
@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        "access": access
    }), error.HTTP_200_OK
