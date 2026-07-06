from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.db import db
from database.models import CompanyProfile, PlacementDrives

bp = Blueprint("company", __name__)


def _get_company_profile(user_id):
    return CompanyProfile.query.filter_by(user_id=user_id).first()


def _serialize_drive(drive):
    return {
        "id": drive.drive_id,
        "jobTitle": drive.job_title,
        "jobDesc": drive.job_desc,
        "eligibility": drive.eligibility,
        "deadline": drive.drive_deadline.isoformat(),
        "status": drive.drive_status,
    }


@bp.route("/status", methods=["GET"])
@jwt_required()
def get_status():
    user_id = int(get_jwt_identity())
    profile = _get_company_profile(user_id)
    if not profile:
        return jsonify({"message": "Company profile not found"}), 404

    return jsonify(
        {
            "companyName": profile.company_name,
            "website": profile.website,
            "hrContact": profile.hr_contact,
            "approvalStatus": profile.approval_status,
            "remarks": profile.remarks,
        }
    ), 200


@bp.route("/drives", methods=["GET"])
@jwt_required()
def list_drives():
    user_id = int(get_jwt_identity())
    profile = _get_company_profile(user_id)
    if not profile:
        return jsonify({"message": "Company profile not found"}), 404

    drives = (
        PlacementDrives.query.filter_by(company_id=profile.company_id)
        .order_by(PlacementDrives.drive_id.desc())
        .all()
    )
    return jsonify([_serialize_drive(d) for d in drives]), 200


@bp.route("/drives", methods=["POST"])
@jwt_required()
def create_drive():
    user_id = int(get_jwt_identity())
    profile = _get_company_profile(user_id)
    if not profile:
        return jsonify({"message": "Company profile not found"}), 404

    if profile.approval_status != "approved":
        return jsonify({"message": "Your company must be approved before posting drives"}), 403

    data = request.get_json() or {}
    required_fields = ["jobTitle", "jobDesc", "eligibility", "deadline"]
    if any(not data.get(field) for field in required_fields):
        return jsonify({"message": "All fields are required"}), 400

    try:
        deadline = datetime.fromisoformat(data.get("deadline"))
    except ValueError:
        return jsonify({"message": "Invalid deadline format"}), 400

    drive = PlacementDrives(
        company_id=profile.company_id,
        job_title=data.get("jobTitle"),
        job_desc=data.get("jobDesc"),
        eligibility=data.get("eligibility"),
        drive_deadline=deadline,
        drive_status="Pending",
    )
    db.session.add(drive)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to create drive", "error": str(e)}), 500

    return jsonify(_serialize_drive(drive)), 201
