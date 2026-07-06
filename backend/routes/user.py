from datetime import datetime

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.models import Applications, PlacementDrives, User

bp = Blueprint("user", __name__)


def _serialize_user(user):
    return {
        "id": user.user_id,
        "email": user.email,
        "mobile": user.mobile,
        "fullName": user.full_name,
        "role": user.role,
    }


@bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(_serialize_user(user)), 200


@bp.route("/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404

    applications = Applications.query.filter_by(student_id=user.user_id).all()

    status_counts = {"applied": 0, "shortlisted": 0, "selected": 0, "rejected": 0}
    for appl in applications:
        if appl.appl_status in status_counts:
            status_counts[appl.appl_status] += 1

    open_drives_count = PlacementDrives.query.filter(
        PlacementDrives.drive_status == "Approved",
        PlacementDrives.drive_deadline >= datetime.utcnow(),
    ).count()

    return jsonify(
        {
            "user": _serialize_user(user),
            "applications": {
                "total": len(applications),
                "statusCounts": status_counts,
            },
            "openDrives": open_drives_count,
        }
    ), 200
