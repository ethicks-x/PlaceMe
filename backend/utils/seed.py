import datetime
import random

from app import app
from database.db import db
from database.models import Applications, CompanyProfile, PlacementDrives, User


def seed_large_dataset():
    print("⏳ Beginning large-scale database seeding...")

    # -------------------------------------------------------------
    # 1. CREATE 22 STUDENTS (Users + StudentProfiles)
    # -------------------------------------------------------------
    first_names = [
        "Liam",
        "Olivia",
        "Noah",
        "Emma",
        "Oliver",
        "Ava",
        "Elijah",
        "Charlotte",
        "William",
        "Sophia",
        "James",
        "Amelia",
        "Benjamin",
        "Isabella",
        "Lucas",
        "Mia",
        "Henry",
        "Evelyn",
        "Alexander",
        "Harper",
        "Mason",
        "Camila",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Martinez",
        "Hernandez",
        "Lopez",
        "Gonzalez",
        "Wilson",
        "Anderson",
        "Thomas",
        "Taylor",
        "Moore",
        "Jackson",
        "Martin",
        "Lee",
        "Perez",
    ]

    students_list = []

    for i in range(22):
        f_name = first_names[i]
        l_name = last_names[i]
        email = f"{f_name.lower()}.{l_name.lower()}@university.edu"
        mobile = f"98765432{i:02d}"

        student_user = User(
            email=email, mobile=mobile, full_name=f"{f_name} {l_name}", role="student"
        )
        student_user.set_password("student123")
        db.session.add(student_user)
        db.session.flush()  # Yields user_id for the profile mapping

        students_list.append(student_user.user_id)

    print("✅ Successfully staged 22 Students.")

    # -------------------------------------------------------------
    # 2. CREATE 20 COMPANIES (Users + CompanyProfiles)
    # -------------------------------------------------------------
    company_names = [
        "TechCorp",
        "InnovaSolutions",
        "QuantumAI",
        "NexusData",
        "ApexSystems",
        "BlueGrid",
        "StellarSoft",
        "CoreMatrix",
        "CyberShield",
        "VanguardDigital",
        "AlphaByte",
        "CloudPulse",
        "DataForge",
        "OmniTech",
        "SummitIT",
        "LogixGlobal",
        "PixelWeb",
        "InfiniteLoop",
        "ZetaSystems",
        "SynapseAI",
    ]
    hr_names = [
        "Robert",
        "Susan",
        "Michael",
        "Mary",
        "David",
        "Jennifer",
        "James",
        "Patricia",
        "John",
        "Linda",
        "Elizabeth",
        "Richard",
        "Barbara",
        "Joseph",
        "Thomas",
        "Charles",
        "Jessica",
        "Christopher",
        "Sarah",
        "Karen",
    ]
    statuses = [
        "approved",
        "approved",
        "approved",
        "pending",
        "rejected",
    ]  # weighted heavily toward approved

    companies_list = []

    for i in range(20):
        c_name = company_names[i]
        hr_name = hr_names[i]
        email = f"recruitment@{c_name.lower()}.com"
        mobile = f"91234567{i:02d}"

        comp_user = User(
            email=email, mobile=mobile, full_name=f"{hr_name} ({c_name} HR)", role="company"
        )
        comp_user.set_password("company123")
        db.session.add(comp_user)

        profile = CompanyProfile(
            company_name=f"{c_name} Inc.",
            hr_contact=mobile,
            website=f"https://{c_name.lower()}.com/careers",
            approval_status=random.choice(statuses),
            remarks="Documents validated and cross-checked by internal placement cell.",
        )
        db.session.add(profile)
        db.session.flush()  # Yields company_id for drives mapping

        # Only companies that are 'approved' can host drives
        if profile.approval_status == "approved":
            companies_list.append(profile.company_id)

    print("✅ Successfully staged 20 Companies.")

    # -------------------------------------------------------------
    # 3. CREATE 20 PLACEMENT DRIVES
    # -------------------------------------------------------------
    job_titles = [
        "Software Engineer Intern",
        "Data Analyst",
        "Frontend Developer",
        "Backend Systems Engineer",
        "Cloud Architecture Intern",
        "Cybersecurity Analyst",
        "DevOps Engineer",
        "Mobile App Developer",
        "Quality Assurance Engineer",
        "Full Stack Specialist",
    ]
    drive_statuses = ["Approved", "Approved", "Closed", "Pending"]

    drives_list = []

    for i in range(20):
        # Pick from our list of approved company IDs
        comp_id = random.choice(companies_list)
        title = random.choice(job_titles)

        drive = PlacementDrives(
            company_id=comp_id,
            job_title=f"{title} ({i + 1})",
            job_desc=f"We are seeking motivated candidates for the position of {title}. \
                        Responsibilities include project deployment, standard testing, \
                        collaborative code architecture reviews, and scaling core applications.",
            eligibility="All Engineering/Technology branches eligible. \
                         Minimum aggregate CGPA >= 7.5. \
                         Strong problem-solving foundations required.",
            drive_deadline=datetime.datetime.now()
            + datetime.timedelta(days=random.randint(5, 30)),
            drive_status=random.choice(drive_statuses),
        )
        db.session.add(drive)
        db.session.flush()  # Yields drive_id for applications mapping

        # Only permit applications to active/approved drives
        if drive.drive_status == "Approved":
            drives_list.append(drive.drive_id)

    print("✅ Successfully staged 20 Placement Drives.")

    # -------------------------------------------------------------
    # 4. CREATE 25 APPLICATIONS (Cross-Linking Students & Active Drives)
    # -------------------------------------------------------------
    appl_statuses = ["applied", "shortlisted", "selected", "rejected", "not applied"]

    existing_applications = set()
    created_applications_count = 0

    while created_applications_count < 25:
        student_id = random.choice(students_list)
        drive_id = random.choice(drives_list)
        pair = (student_id, drive_id)

        if pair not in existing_applications:
            existing_applications.add(pair)

            application = Applications(
                student_id=student_id,
                drive_id=drive_id,
                appl_status=random.choice(appl_statuses),
                appl_date=datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 4)),
            )
            db.session.add(application)
            created_applications_count += 1

    print("✅ Successfully staged 25 Dynamic Application Ties.")

    # -------------------------------------------------------------
    # 5. COMMIT EVERYTHING TO THE DB FILE
    # -------------------------------------------------------------
    try:
        db.session.commit()
        print("\n🚀 SUCCESS! The database has been populated with datasets.")
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ SEED FAILURE! Database state changes rolled back clean. Reason: {e}")


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

        seed_large_dataset()
