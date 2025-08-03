from flask import Blueprint, request, jsonify, url_for, redirect
from models import db, User, Todo
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flask_mail import Message


def create_blueprints(google, mail):
    auth_bp = Blueprint("auth", __name__)
    todo_bp = Blueprint("todo", __name__)

    # ---------- AUTH ROUTES ----------
    @auth_bp.route("/register", methods=["POST"])
    def register():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "Email already exists"}), 400

        new_user = User(email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully"}), 201

    @auth_bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access = create_access_token(identity=str(user.id))
            refresh = create_refresh_token(identity=str(user.id))
            return jsonify({
                "access_token": access,
                "refresh_token": refresh,
                "email": user.email
            }), 200

        return jsonify({"msg": "Invalid credentials"}), 401

    # ---------- GOOGLE OAUTH ----------
    @auth_bp.route("/google/login")
    def google_login_start():
        redirect_uri = url_for("auth.google_callback", _external=True)
        return google.authorize_redirect(redirect_uri)

    @auth_bp.route("/google/callback")
    def google_callback():
        token = google.authorize_access_token()
        resp = google.get("https://openidconnect.googleapis.com/v1/userinfo")
        user_info = resp.json()

        email = user_info.get("email")
        name = user_info.get("name")
        picture = user_info.get("picture")

        if not email:
            return jsonify({"msg": "Failed to retrieve Google account info"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            user.set_password("google-oauth")
            db.session.add(user)
            db.session.commit()

        access = create_access_token(identity=str(user.id))
        refresh = create_refresh_token(identity=str(user.id))

        frontend_url = "https://to-do-6-2awb.onrender.com/login"
        return redirect(
            f"{frontend_url}?access={access}&refresh={refresh}&email={email}&name={name}&picture={picture}"
        )

    # ---------- REFRESH TOKEN ----------
    @auth_bp.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        current_user = get_jwt_identity()
        new_access = create_access_token(identity=current_user)
        return jsonify({"access_token": new_access}), 200

    # ---------- TODO ROUTES ----------
    @todo_bp.route("/", methods=["GET"])
    @jwt_required()
    def get_todos():
        user_id = int(get_jwt_identity())
        todos = Todo.query.filter_by(user_id=user_id).all()
        return jsonify([
            {
                "id": t.id,
                "title": t.title,
                "created_at": t.created_at.isoformat(),
                "completed": t.completed
            }
            for t in todos
        ])

    @todo_bp.route("/", methods=["POST"])
    @jwt_required()
    def create_todo():
        data = request.get_json()
        user_id = int(get_jwt_identity())
        todo = Todo(title=data.get("title"), user_id=user_id)
        db.session.add(todo)
        db.session.commit()
        return jsonify({"msg": "Todo created"}), 201

    @todo_bp.route("/<int:todo_id>", methods=["PUT"])
    @jwt_required()
    def update_todo(todo_id):
        user_id = int(get_jwt_identity())
        data = request.get_json()
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

        if not todo:
            return jsonify({"msg": "Todo not found"}), 404

        todo.title = data.get("title", todo.title)
        db.session.commit()
        return jsonify({"msg": "Todo updated"}), 200

    @todo_bp.route("/<int:todo_id>", methods=["DELETE"])
    @jwt_required()
    def delete_todo(todo_id):
        user_id = int(get_jwt_identity())
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
        if not todo:
            return jsonify({"msg": "Todo not found"}), 404

        db.session.delete(todo)
        db.session.commit()
        return jsonify({"msg": "Todo deleted"}), 200

    @todo_bp.route("/<int:todo_id>/complete", methods=["PUT"])
    @jwt_required()
    def complete_todo(todo_id):
        user_id = int(get_jwt_identity())
        todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

        if not todo:
            return jsonify({"msg": "Todo not found"}), 404

        todo.completed = True
        db.session.commit()

        user = User.query.get(user_id)
        msg = Message(
            subject="✅ Task Completed!",
            recipients=[user.email],
            body=f"Good job! You have completed your task: {todo.title}"
        )
        mail.send(msg)

        return jsonify({"msg": "Todo marked completed and email sent!"}), 200

    # ✅ return blueprints at the end
    return auth_bp, todo_bp
