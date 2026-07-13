from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.db import db
from database.models import Applications, CompanyProfile, PlacementDrives, StudentProfile, User

bp = Blueprint("user", __name__)


def _serialize_user(user):
    data = {
        "id": user.user_id,
        "email": user.email,
        "mobile": user.mobile,
        "fullName": user.full_name,
        "role": user.role,
    }

    if user.role == "student":
        profile = StudentProfile.query.filter_by(user_id=user.user_id).first()
        missing_fields = _missing_profile_fields(user.user_id)
        data.update(
            {
                "degree": profile.degree if profile else None,
                "graduationYear": profile.graduation_year if profile else None,
                "cgpa": profile.cgpa if profile else None,
                "resumeUrl": profile.resume_url if profile else None,
                "skills": profile.skills if profile else None,
                "bio": profile.bio if profile else None,
                "profileComplete": not missing_fields,
                "missingProfileFields": missing_fields,
            }
        )

    return data


REQUIRED_PROFILE_FIELDS = (
    ("degree", "Degree"),
    ("graduation_year", "Graduation Year"),
    ("cgpa", "CGPA"),
    ("resume_url", "Resume URL"),
)


def _missing_profile_fields(user_id):
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if not profile:
        return [label for _, label in REQUIRED_PROFILE_FIELDS]
    return [
        label for field, label in REQUIRED_PROFILE_FIELDS if getattr(profile, field) in (None, "")
    ]


def ineligibility_check(drive, profile):
    if drive.min_cgpa is not None:
        if not profile or profile.cgpa is None:
            return f"Requires a minimum CGPA of {drive.min_cgpa}"
        if profile.cgpa < drive.min_cgpa:
            return f"Your CGPA ({profile.cgpa}) is below the required {drive.min_cgpa}"

    if drive.eligible_graduation_year is not None:
        if not profile or profile.graduation_year is None:
            return f"Open only to the {drive.eligible_graduation_year} graduating batch"
        if profile.graduation_year != drive.eligible_graduation_year:
            return f"Open only to the {drive.eligible_graduation_year} graduating batch"

    return None


def _serialize_drive(drive, applied_drive_ids, profile):
    company = CompanyProfile.query.get(drive.company_id)
    ineligible_reason = ineligibility_check(drive, profile)
    return {
        "id": drive.drive_id,
        "jobTitle": drive.job_title,
        "jobDesc": drive.job_desc,
        "eligibility": drive.eligibility,
        "minCgpa": drive.min_cgpa,
        "eligibleGraduationYear": drive.eligible_graduation_year,
        "deadline": drive.drive_deadline.isoformat(),
        "companyName": company.company_name if company else "Unknown",
        "hasApplied": drive.drive_id in applied_drive_ids,
        "isExpired": drive.drive_deadline < datetime.utcnow(),
        "isEligible": ineligible_reason is None,
        "ineligibleReason": ineligible_reason,
    }


@bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(_serialize_user(user)), 200


@bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json() or {}
    full_name = data.get("fullName")
    mobile = data.get("mobile")

    if mobile and mobile != user.mobile:
        if User.query.filter_by(mobile=mobile).first():
            return jsonify({"message": "This mobile number is already in use"}), 409
        user.mobile = mobile

    if full_name:
        user.full_name = full_name

    if user.role == "student":
        profile = StudentProfile.query.filter_by(user_id=user.user_id).first()
        if not profile:
            profile = StudentProfile(user_id=user.user_id)
            db.session.add(profile)

        if "degree" in data:
            profile.degree = data.get("degree") or None
        if "graduationYear" in data:
            grad_year = data.get("graduationYear")
            try:
                profile.graduation_year = int(grad_year) if grad_year not in (None, "") else None
            except TypeError, ValueError:
                return jsonify({"message": "Graduation year must be a number"}), 400
        if "cgpa" in data:
            cgpa = data.get("cgpa")
            try:
                profile.cgpa = float(cgpa) if cgpa not in (None, "") else None
            except TypeError, ValueError:
                return jsonify({"message": "CGPA must be a number"}), 400
        if "resumeUrl" in data:
            profile.resume_url = data.get("resumeUrl") or None
        if "skills" in data:
            profile.skills = data.get("skills") or None
        if "bio" in data:
            profile.bio = data.get("bio") or None

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update profile.", "error": str(e)}), 500

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


@bp.route("/drives", methods=["GET"])
@jwt_required()
def list_drives():
    user_id = int(get_jwt_identity())

    drives = (
        PlacementDrives.query.filter_by(drive_status="Approved")
        .order_by(PlacementDrives.drive_deadline)
        .all()
    )
    applied_drive_ids = {
        appl.drive_id for appl in Applications.query.filter_by(student_id=user_id).all()
    }
    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    return jsonify([_serialize_drive(drive, applied_drive_ids, profile) for drive in drives]), 200


@bp.route("/drives/<int:drive_id>/apply", methods=["POST"])
@jwt_required()
def apply_to_drive(drive_id):
    user_id = int(get_jwt_identity())

    drive = PlacementDrives.query.get(drive_id)
    if not drive or drive.drive_status != "Approved":
        return jsonify({"message": "This drive is not open for applications"}), 404

    if drive.drive_deadline < datetime.utcnow():
        return jsonify({"message": "The application deadline has passed"}), 400

    missing_fields = _missing_profile_fields(user_id)
    if missing_fields:
        return jsonify(
            {
                "message": (
                    "Please complete your profile before applying. Missing: "
                    + ", ".join(missing_fields)
                )
            }
        ), 400

    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    ineligible_reason = ineligibility_check(drive, profile)
    if ineligible_reason:
        return jsonify(
            {"message": f"You are not eligible for this drive: {ineligible_reason}"}
        ), 403

    if Applications.query.filter_by(student_id=user_id, drive_id=drive_id).first():
        return jsonify({"message": "You have already applied to this drive"}), 409

    application = Applications(student_id=user_id, drive_id=drive_id, appl_status="applied")
    db.session.add(application)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to submit application", "error": str(e)}), 500

    return jsonify({"message": "Application submitted successfully"}), 201


@bp.route("/applications", methods=["GET"])
@jwt_required()
def list_applications():
    user_id = int(get_jwt_identity())

    applications = (
        Applications.query.filter_by(student_id=user_id)
        .order_by(Applications.appl_date.desc())
        .all()
    )

    result = []
    for appl in applications:
        drive = PlacementDrives.query.get(appl.drive_id)
        company = CompanyProfile.query.get(drive.company_id) if drive else None
        result.append(
            {
                "id": appl.appl_id,
                "jobTitle": drive.job_title if drive else "Unknown",
                "companyName": company.company_name if company else "Unknown",
                "appliedDate": appl.appl_date.isoformat(),
                "status": appl.appl_status,
            }
        )

    return jsonify(result), 200
