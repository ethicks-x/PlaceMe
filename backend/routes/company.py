from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.models import CompanyProfile

bp = Blueprint("company", __name__)


@bp.route("/status", methods=["GET"])
@jwt_required()
def get_status():
    user_id = int(get_jwt_identity())
    profile = CompanyProfile.query.filter_by(user_id=user_id).first()
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
