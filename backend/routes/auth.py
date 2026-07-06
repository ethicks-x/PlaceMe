from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

from database.db import db
from database.models import CompanyProfile, User

bp = Blueprint("auth", __name__)


def _issue_token_response(user):
    additional_claims = {"role": user.role}
    access_token = create_access_token(
        identity=str(user.user_id), additional_claims=additional_claims
    )
    user_data = {
        "id": user.user_id,
        "email": user.email,
        "mobile": user.mobile,
        "fullName": user.full_name,
        "role": user.role,
    }
    return access_token, user_data


def create_admin_user():
    admin_email = "admin@sinu.in"
    admin_mobile = "9874297650"
    admin_password = "oybr85010"
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        try:
            new_admin = User(
                email=admin_email, mobile=admin_mobile, full_name="Admin User", role="admin"
            )
            new_admin.set_password(admin_password)
            db.session.add(new_admin)
            db.session.commit()
            print("Admin user created successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")
    else:
        print("Admin user already exists.")


@bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "This email is already registered"}), 409

    # Create New User
    try:
        new_user = User(
            email=data.get("email"),
            mobile=data.get("mobile"),
            full_name=data.get("full_name"),
            role="student",
        )
        new_user.set_password(data.get("password"))  # Hash the password

        db.session.add(new_user)
        db.session.commit()

        access_token, user_data = _issue_token_response(new_user)

        return jsonify(access_token=access_token, user=user_data), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred during registration.", "error": str(e)}), 500


@bp.route("/register-company", methods=["POST"])
def register_company():
    data = request.get_json()

    required_fields = ["email", "password", "companyName", "website", "hrContact", "hrMobile"]
    if not data or any(not data.get(field) for field in required_fields):
        return jsonify({"message": "All fields are required"}), 400

    if User.query.filter_by(email=data.get("email")).first():
        return jsonify({"message": "This email is already registered"}), 409

    if User.query.filter_by(mobile=data.get("hrMobile")).first():
        return jsonify({"message": "This mobile number is already registered"}), 409

    if CompanyProfile.query.filter_by(company_name=data.get("companyName")).first():
        return jsonify({"message": "This company name is already registered"}), 409

    try:
        new_user = User(
            email=data.get("email"),
            mobile=data.get("hrMobile"),
            full_name=data.get("hrContact"),
            role="company",
        )
        new_user.set_password(data.get("password"))
        db.session.add(new_user)
        db.session.flush()  # Yields user_id for the profile mapping

        profile = CompanyProfile(
            user_id=new_user.user_id,
            company_name=data.get("companyName"),
            hr_contact=data.get("hrMobile"),
            website=data.get("website"),
            approval_status="pending",
            remarks="Awaiting admin review.",
        )
        db.session.add(profile)
        db.session.commit()

        access_token, user_data = _issue_token_response(new_user)

        return jsonify(access_token=access_token, user=user_data), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred during registration.", "error": str(e)}), 500


@bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    remember_me = data.get("rememberMe", False)

    print(f"Login attempt for email: {email}, rememberMe: {remember_me}")

    if not data or not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    print(f"User found: {user}")

    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token, user_data = _issue_token_response(user)

    if remember_me:
        response = make_response(jsonify(user=user_data, msg="Login successful"))
        set_access_cookies(response, access_token, max_age=60 * 60 * 24 * 10)
        return response, 200
    else:
        return jsonify(access_token=access_token, user=user_data), 200


@bp.route("/logout", methods=["POST"])
def logout_user():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200
