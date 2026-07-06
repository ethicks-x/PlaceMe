from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy import or_

from database.db import db
from database.models import Applications, CompanyProfile, PlacementDrives, User

bp = Blueprint("admin", __name__)


def admin_required(fn):
    @jwt_required()
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if get_jwt().get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)

    return wrapper


def _serialize_company(profile):
    user = User.query.get(profile.user_id)
    return {
        "id": profile.company_id,
        "userId": profile.user_id,
        "companyName": profile.company_name,
        "hrContact": profile.hr_contact,
        "website": profile.website,
        "approvalStatus": profile.approval_status,
        "remarks": profile.remarks,
        "email": user.email if user else None,
        "isActive": user.is_active if user else None,
    }


def _serialize_student(user):
    return {
        "id": user.user_id,
        "fullName": user.full_name,
        "email": user.email,
        "mobile": user.mobile,
        "isActive": user.is_active,
    }


def _serialize_drive(drive):
    company = CompanyProfile.query.get(drive.company_id)
    return {
        "id": drive.drive_id,
        "jobTitle": drive.job_title,
        "jobDesc": drive.job_desc,
        "eligibility": drive.eligibility,
        "deadline": drive.drive_deadline.isoformat(),
        "status": drive.drive_status,
        "companyName": company.company_name if company else "Unknown",
    }


# ---------- Companies ----------


@bp.route("/companies", methods=["GET"])
@admin_required
def list_companies():
    status = request.args.get("status")
    search = request.args.get("search", "").strip()

    query = CompanyProfile.query
    if status:
        query = query.filter_by(approval_status=status)
    if search:
        query = query.filter(CompanyProfile.company_name.ilike(f"%{search}%"))

    companies = query.order_by(CompanyProfile.company_id.desc()).all()
    return jsonify([_serialize_company(c) for c in companies]), 200


@bp.route("/companies/<int:company_id>/approve", methods=["POST"])
@admin_required
def approve_company(company_id):
    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    company.approval_status = "approved"
    db.session.commit()
    return jsonify(_serialize_company(company)), 200


@bp.route("/companies/<int:company_id>/reject", methods=["POST"])
@admin_required
def reject_company(company_id):
    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    data = request.get_json() or {}
    company.approval_status = "rejected"
    company.remarks = data.get("remarks") or "Rejected by admin."
    db.session.commit()
    return jsonify(_serialize_company(company)), 200


@bp.route("/companies/<int:company_id>/activate", methods=["POST"])
@admin_required
def activate_company(company_id):
    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    user = User.query.get(company.user_id)
    user.is_active = True
    db.session.commit()
    return jsonify(_serialize_company(company)), 200


@bp.route("/companies/<int:company_id>/deactivate", methods=["POST"])
@admin_required
def deactivate_company(company_id):
    company = CompanyProfile.query.get(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404

    user = User.query.get(company.user_id)
    user.is_active = False
    db.session.commit()
    return jsonify(_serialize_company(company)), 200


# ---------- Students ----------


@bp.route("/students", methods=["GET"])
@admin_required
def list_students():
    search = request.args.get("search", "").strip()

    query = User.query.filter_by(role="student")
    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(User.full_name.ilike(like), User.email.ilike(like), User.mobile.ilike(like))
        )

    students = query.order_by(User.user_id.desc()).all()
    return jsonify([_serialize_student(s) for s in students]), 200


@bp.route("/students/<int:user_id>/activate", methods=["POST"])
@admin_required
def activate_student(user_id):
    user = User.query.filter_by(user_id=user_id, role="student").first()
    if not user:
        return jsonify({"message": "Student not found"}), 404

    user.is_active = True
    db.session.commit()
    return jsonify(_serialize_student(user)), 200


@bp.route("/students/<int:user_id>/deactivate", methods=["POST"])
@admin_required
def deactivate_student(user_id):
    user = User.query.filter_by(user_id=user_id, role="student").first()
    if not user:
        return jsonify({"message": "Student not found"}), 404

    user.is_active = False
    db.session.commit()
    return jsonify(_serialize_student(user)), 200


# ---------- Drives ----------


@bp.route("/drives", methods=["GET"])
@admin_required
def list_drives():
    status = request.args.get("status")

    query = PlacementDrives.query
    if status:
        query = query.filter_by(drive_status=status)

    drives = query.order_by(PlacementDrives.drive_id.desc()).all()
    return jsonify([_serialize_drive(d) for d in drives]), 200


@bp.route("/drives/<int:drive_id>/approve", methods=["POST"])
@admin_required
def approve_drive(drive_id):
    drive = PlacementDrives.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.drive_status = "Approved"
    db.session.commit()
    return jsonify(_serialize_drive(drive)), 200


@bp.route("/drives/<int:drive_id>/reject", methods=["POST"])
@admin_required
def reject_drive(drive_id):
    drive = PlacementDrives.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.drive_status = "Rejected"
    db.session.commit()
    return jsonify(_serialize_drive(drive)), 200


# ---------- Stats ----------


@bp.route("/stats", methods=["GET"])
@admin_required
def get_stats():
    total_students = User.query.filter_by(role="student").count()
    total_companies = CompanyProfile.query.count()

    companies_by_status = {
        status: CompanyProfile.query.filter_by(approval_status=status).count()
        for status in ("pending", "approved", "rejected")
    }

    drives_by_status = {
        status: PlacementDrives.query.filter_by(drive_status=status).count()
        for status in ("Pending", "Approved", "Rejected", "Closed")
    }

    applications_by_status = {
        status: Applications.query.filter_by(appl_status=status).count()
        for status in ("applied", "shortlisted", "selected", "rejected")
    }

    total_applications = sum(applications_by_status.values())
    placement_rate = (
        round(applications_by_status["selected"] / total_students * 100, 1)
        if total_students
        else 0
    )

    return jsonify(
        {
            "totalStudents": total_students,
            "totalCompanies": total_companies,
            "companiesByStatus": companies_by_status,
            "drivesByStatus": drives_by_status,
            "totalApplications": total_applications,
            "applicationsByStatus": applications_by_status,
            "placementRate": placement_rate,
        }
    ), 200
