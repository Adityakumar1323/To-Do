from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from models import db
from authlib.integrations.flask_client import OAuth
from routes import create_blueprints
from flask_cors import CORS
from flask_mail import Mail
import os

app = Flask(__name__)

# ---------- Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

# 🔑 Required for Google OAuth session handling
app.secret_key = os.getenv("FLASK_SECRET_KEY", "my-dev-secret-key")

# ---------- CORS (Frontend URLs allowed) ----------
CORS(app,
     supports_credentials=True,
     resources={
         r"/api/*": {
             "origins": [
                 "http://localhost:5173",
                 "http://127.0.0.1:5173",
                 "https://to-do-6-2awb.onrender.com"
             ]
         }
     })

# ---------- OAuth setup ----------
oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id="76610639739-ekq368m7d44r5q1figakdi9qr7da59hq.apps.googleusercontent.com",
    client_secret="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",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# ---------- Email Setup ----------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "adi484841@gmail.com")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", "kzlukqvbeysktyhe")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER", "adi484841@gmail.com")

mail = Mail(app)

# ---------- Init DB & JWT ----------
db.init_app(app)
jwt = JWTManager(app)

# ---------- Register Blueprints ----------
auth_bp, todo_bp = create_blueprints(google, mail)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(todo_bp, url_prefix="/api/todo")
@app.route("/healthz")
def health_check():
    return "ok", 200


# ---------- Run ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
