from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.db import db
from database.models import Applications, CompanyProfile, PlacementDrives, StudentProfile, User

bp = Blueprint("company", __name__)

APPL_ST = {"applied", "shortlisted", "selected", "rejected"}


def _get_company_profile(user_id):
    return CompanyProfile.query.filter_by(user_id=user_id).first()


def _serialize_drive(drive):
    appl_count = Applications.query.filter_by(drive_id=drive.drive_id).count()
    return {
        "id": drive.drive_id,
        "jobTitle": drive.job_title,
        "jobDesc": drive.job_desc,
        "eligibility": drive.eligibility,
        "deadline": drive.drive_deadline.isoformat(),
        "status": drive.drive_status,
        "applicationCount": appl_count,
    }


def _serialize_applicant(appl):
    student = User.query.get(appl.student_id)
    profile = StudentProfile.query.filter_by(user_id=appl.student_id).first()
    return {
        "id": appl.appl_id,
        "studentName": student.full_name if student else "unknown",
        "studentEmail": student.email if student else "unknown",
        "studentMobile": student.mobile if student else "unknown",
        "appliedDate": appl.appl_date.isoformat(),
        "status": appl.appl_status,
        "degree": profile.degree if profile else None,
        "graduationYear": profile.graduation_year if profile else None,
        "cgpa": profile.cgpa if profile else None,
        "resumeUrl": profile.resume_url if profile else None,
        "skills": profile.skills if profile else None,
        "bio": profile.bio if profile else None,
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


@bp.route("/drives/<int:drive_id>/applicants", methods=["GET"])
@jwt_required()
def list_applicants(drive_id):
    user_id = int(get_jwt_identity())
    profile = _get_company_profile(user_id)
    if not profile:
        return jsonify({"message": "Company profile not found"}), 404

    drive = PlacementDrives.query.get(drive_id)
    if not drive or drive.company_id != profile.company_id:
        return jsonify({"message": "Drive not found"}), 404

    applications = (
        Applications.query.filter_by(drive_id=drive_id)
        .order_by(Applications.appl_date.desc())
        .all()
    )

    return jsonify(
        {
            "drive": _serialize_drive(drive),
            "applicants": [_serialize_applicant(appl) for appl in applications],
        }
    ), 200


@bp.route("/applications/<int:appl_id>/status", methods=["PUT"])
@jwt_required()
def update_application_status(appl_id):
    user_id = int(get_jwt_identity())
    profile = _get_company_profile(user_id)
    if not profile:
        return jsonify({"message": "Company profile not found"}), 404

    application = Applications.query.get(appl_id)
    if not application:
        return jsonify({"message": "Application not found"}), 404

    drive = PlacementDrives.query.get(application.drive_id)
    if not drive or drive.company_id != profile.company_id:
        return jsonify({"message": "Application not found"}), 404

    data = request.get_json(silent=True) or {}
    new_status = data.get("status")
    if new_status not in APPL_ST:
        return jsonify({"message": f"Status must be one of: {', '.join(sorted(APPL_ST))}"}), 400

    application.appl_status = new_status

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Application status update error: {e}")
        return jsonify({"message": "Failed to update the application. Please try again."}), 500

    return jsonify(_serialize_applicant(application)), 200
