import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from database.db import create_migration, db
from routes import auth, user
from routes.auth import create_admin_user

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__, static_folder="static", subdomain_matching=False)

# This allows the server to accept requests from different origins,
# which is useful for APIs.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.config.from_object(__name__)

jwt = JWTManager(app)
# App Config
app.config["SERVER_NAME"] = os.getenv("SERVER_NAME")
app.url_map.default_subdomain = ""

app.secret_key = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)  # Set to 12 hours


# Initialize the Bcrypt extension
# This will be used to hash passwords securely.
bcrypt = Bcrypt(app)
app.config["BCRYPT"] = bcrypt

db_path = Path.cwd() / "database/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(db_path / "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
create_migration(app)

app.register_blueprint(auth.bp, url_prefix="/api/auth")
app.register_blueprint(user.bp, url_prefix="/api")

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()

            create_admin_user()

        server_host = os.getenv("SERVER_HOST")
        server_port = os.getenv("SERVER_PORT")
        server_debug = os.getenv("SERVER_DEBUG")

        app.run(host=server_host, port=server_port, debug=bool(server_debug))

    except Exception as e:
        print(f"An error occurred: {e}")
