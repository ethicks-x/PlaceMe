from flask import current_app

from .db import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(12), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    role = db.Column(
        db.Enum("student", "company", "admin", name="role_enum"),
        nullable=False,
        default="student",
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        bcrypt = current_app.config["BCRYPT"]
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        bcrypt = current_app.config["BCRYPT"]
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.user_id} {self.email} ({self.role})>"


class CompanyProfile(db.Model):
    __tablename__ = "company_profile"

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    hr_contact = db.Column(db.String(12), unique=True, nullable=False)
    website = db.Column(db.String(128), unique=True, nullable=False)
    approval_status = db.Column(
        db.Enum("pending", "approved", "rejected", name="company_approval"),
        nullable=False,
        default="pending",
    )
    remarks = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<Company {self.company_id} {self.company_name} {self.website}>"


class PlacementDrives(db.Model):
    __tablename__ = "placement_drives"

    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company_profile.company_id"), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_desc = db.Column(db.String(300), nullable=False)
    eligibility = db.Column(db.String(150), nullable=False)
    drive_deadline = db.Column(db.DateTime, nullable=False)
    drive_status = db.Column(
        db.Enum("Pending", "Approved", "Closed", name="drive_status"),
        nullable=False,
        default="Pending",
    )

    def __repr__(self):
        return f"Placement Drive: {self.drive_id} {self.drive_deadline} {self.drive_status}"


class Applications(db.Model):
    __tablename__ = "applications"

    appl_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.drive_id"), nullable=False)
    appl_date = db.Column(db.DateTime, nullable=False)
    appl_status = db.Column(
        db.Enum(
            "not applied", "applied", "shortlisted", "selected", "rejected", name="appl_status"
        ),
        nullable=False,
        default="not applied",
    )

    def __repr__(self):
        return f"Application: {self.appl_id} {self.appl_date} {self.appl_status}"
